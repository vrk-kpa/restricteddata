import { access } from "node:fs";
import { rm } from "node:fs/promises";
import gulp from "gulp";
import { exec } from "child_process";
import imagemin, { gifsicle, mozjpeg, optipng, svgo } from 'gulp-imagemin';
import cleancss from "gulp-clean-css";
import gulpStylelint from "@ronilaukkarinen/gulp-stylelint";
import * as dartSass from 'sass';
import gulpSass from 'gulp-sass';
import rename from "gulp-rename";

const { src, watch, dest, parallel, lastRun, series } = gulp;
const sass = gulpSass(dartSass);

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

// Check if the file exists in the current directory.
access(new URL(paths.src.fontawesome, rootDir), (err) => {
  paths.src.fontawesome = "node_modules/@fortawesome/fontawesome-free/";
});

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

const rebuildCkanWebassets = async () => {
  // Fetch docker container name with the subcommand $(docker ps -f "name=ckan-1" --format {{.Names}})
  // and run ckan asset build within the found container to update webassets for easier development
  return exec('docker exec $(docker ps -f "name=ckan-1" --format {{.Names}}) ckan asset build', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`${stdout}`);
  });
}

export const lint = () => {
  return src(paths.src.scss + "**/*.scss", { since: lastRun(lint) })
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
    .pipe(dest(paths.ckanPublic + "css"))
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

const fonts = () => {
  return src(paths.src.fonts + "**/*", { since: lastRun(fonts) })
    .pipe(dest(paths.ckanPublic + "fonts"))
};

const javascript = () => {
  return src([paths.src.javascript + "**/*"], { since: lastRun(javascript) })
    .pipe(dest(paths.ckanAssets + "javascript"))
};

const libs = () => {
  let nodeLibs = ['select2']
  const libPaths = nodeLibs.map((libName) => {
    return "node_modules/" + libName + "/**/*";
  })
  return src(libPaths, { base: "./node_modules/" }, { since: lastRun(libs) })
    .pipe(dest(paths.ckanAssets + "vendor/"))
}
const copyFontawesome = () => {
  return src(paths.src.fontawesome + "/**/*")
    .pipe(dest(paths.ckanPublic + "/vendor/@fortawesome/fontawesome"))
}

function watchFiles() {
  watch(paths.src.src + "**/*", { ignoreInitial: false }, localBuild);
}
export { watchFiles as watch }

export const build = parallel(ckanSass, javascript, libs, images, fonts, fontsCss, copyFontawesome);
export const localBuild = series(lint, build, rebuildCkanWebassets);

export default build
