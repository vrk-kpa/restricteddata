
import gulp from "gulp";
import { exec } from "node:child_process";
import { rm } from "node:fs/promises";
import { promisify } from "node:util";
import * as dartSass from 'sass';
import gulpSass from 'gulp-sass';
import imagemin, { gifsicle, mozjpeg, optipng, svgo } from 'gulp-imagemin';
import cleancss from "gulp-clean-css";
import rename from "gulp-rename";
import gulpStylelint from "@ronilaukkarinen/gulp-stylelint";

const { src, watch, dest, parallel, lastRun, series } = gulp;
const sass = gulpSass(dartSass);
const promisedExec = promisify(exec);

const rootDir = new URL('./', import.meta.url)

const paths = {
  src: {
    src: "assets/src/",
    images: "assets/src/images/",
    scss: "assets/src/scss/",
    fonts: "assets/src/fonts/",
    javascript: "assets/src/javascript/",
    fontawesome: "node_modules/@fortawesome/fontawesome-pro/",
  },
  ckanAssets: "ckan/ckanext/ckanext-registrydata/ckanext/registrydata/assets/",
  ckanPublic: "ckan/ckanext/ckanext-registrydata/ckanext/registrydata/public/"
};

// Delete any previously generated assets
export async function clean() {
  const removables = [
    new URL(paths.ckanAssets + 'css/', rootDir),
    new URL(paths.ckanAssets + 'javascript/', rootDir),
    new URL(paths.ckanAssets + 'vendor/', rootDir),
    new URL(paths.ckanPublic + 'css/', rootDir),
    new URL(paths.ckanPublic + 'images/', rootDir),
    new URL(paths.ckanPublic + 'fonts/', rootDir),
    new URL(paths.ckanPublic + 'vendor/', rootDir),
  ];
  const promises = removables.map((path) => {
    rm(path, {
      recursive: true,
      force: true
    });
  })
  await Promise.all(promises);
};

// Rebuild ckan webassets to see your changes as webassets are generated only once and cached
const rebuildCkanWebassets = async () => {
  // Fetch docker container name with the subcommand $(docker ps -f "name=ckan-1" --format {{.Names}})
  // and run ckan asset build within the found container to update webassets for easier development
  const { stdout } = await promisedExec('docker exec $(docker ps -f "name=ckan-1" --format {{.Names}}) ckan asset build')
  console.log(`   [rebuildCkanWebassets]: ${stdout}`.trimEnd());
}

// Lint scss
export const lintStyles = () => {
  return src(paths.src.scss + "**/*.scss", { since: lastRun(lintStyles) })
    .pipe(gulpStylelint({
      fix: true,
      failAfterError: true,
      reporters: [
        { formatter: 'verbose', console: true }
      ]
    }))
};

// Preprocess our ckan sass
const ckanSass = () => {
  return src(paths.src.scss + "ckan/**/*.scss", { sourcemaps: true, since: lastRun(ckanSass) })
    .pipe(sass({ includePaths: ["node_modules"], outputStyle: 'expanded', sourceMap: true }).on('error', sass.logError))
    .pipe(cleancss({ keepBreaks: false }))
    .pipe(rename('registrydata.css'))
    .pipe(dest(paths.ckanAssets + "css", { sourcemaps: './maps' }))
};

// Separate fonts to their own css to optimize their loading
const fontsCss = () => {
  return src(paths.src.scss + "fonts.scss", { since: lastRun(fontsCss) })
    .pipe(sass({ includePaths: ["node_modules"], outputStyle: 'expanded' }).on('error', sass.logError))
    .pipe(cleancss({ keepBreaks: false }))
    .pipe(rename('fonts.css'))
    .pipe(dest(paths.ckanPublic + "fonts"))
};

// Optimize images
const images = () => {
  return src(paths.src.images + "**/*", { since: lastRun(images) })
    .pipe(imagemin([
      gifsicle({ interlaced: true }),
      mozjpeg({ quality: 75, progressive: true }),
      optipng({ optimizationLevel: 5 }),
      svgo({
        plugins: [
          {
            name: 'removeViewBox',
            active: true
          },
          {
            name: 'cleanupIDs',
            active: false
          }
        ]
      })
    ]))
    .pipe(dest(paths.ckanPublic + "images"))
};

// Copy fonts
const fonts = () => {
  return src(paths.src.fonts + "**/*", { since: lastRun(fonts) })
    .pipe(dest(paths.ckanPublic + "fonts"))
};

// Copy src javascript
const javascript = () => {
  return src([paths.src.javascript + "**/*"], { since: lastRun(javascript) })
    .pipe(dest(paths.ckanAssets + "javascript"))
};

const copyFontawesomeCss = () => {
  return src(paths.src.fontawesome + "css/all.css", { since: lastRun(copyFontawesomeCss), allowEmpty: true })
    .pipe(dest(paths.ckanAssets + "/vendor/fontawesome/css/"))
}

const copyFontawesomeFonts = () => {
  return src(paths.src.fontawesome + "webfonts/*", { since: lastRun(copyFontawesomeFonts) })
    .pipe(dest(paths.ckanPublic + "/vendor/fontawesome/webfonts/"))
}

const copyFontawesome = parallel(copyFontawesomeCss, copyFontawesomeFonts)

// Lint things (scss, js, etc)
export const lint = parallel(lintStyles)

// Simplified build (default export for CI)
export const build = parallel(ckanSass, javascript, images, fonts, fontsCss, copyFontawesome);

// Add linting and rebuilding ckan webassets when building locally
export const localBuild = series(lint, build, rebuildCkanWebassets);

// Watch for any file changes in the assets/src folder (javascript, css, images, fonts) and rebuild the assets
function watchFiles() {
  watch(paths.src.src + "**/*", { ignoreInitial: false }, localBuild);
}
export { watchFiles as watch }

export default build
