// Flips '* label' into 'label *'
(function ($, window) {
  $(() => {
    window.ckan.sandbox().subscribe("slug-preview-created", (el) => {
      const content = $(el).find("strong").contents();
      let [required, label] = content;
      required.remove();
      label.data = label.data.trim().replace(":", ": ");
      label.after(required);
    });
  });
})(this.jQuery, this);
