/* An multi-input module that allows to add repeating text-inputs on form
 *
 * linkText - Text/Translation-key that should be used for add-button
 * linkIcon - Fontawesome icon-class for i-element that is added before linkText inside add button
 *          - Set false, if you don't want to show icon
 *
 * Examples
 *
 *   // <input name="example" data-module="restricteddata_input_multiple" data-module-link-text="{{ _("Add link") }}" data-module-link-icon="fa-globe" />
 *   // <input name="example" data-module="restricteddata_input_multiple" data-module-link-text="{{ _("Add link")}}" data-module-link-icon="false" />
 *
 */
ckan.module("restricteddata_input_multiple", function ($) {
  return {
    options: {
      linktext: 'Add link',
      linkicon: 'fa-globe',
    },
    initialize: function () {
      var module = this;
      var addLinkText = module._(module.options.linktext);
      $(function () {
        /** Get container element of current multiple-value-group */
        var $multiValueContainer = $(module.el).parent().parent();

        /** If multivalue buttons are already initialized, stop execution */
        if ($multiValueContainer.data('module-initialized') === true) {
          return;
        }
        /** Create addLink after inputs */
        var $addLink = $(`
          <button type="button" class="btn-link">${module.options.linkicon !== false ? `<i class="fa ${module.options.linkicon}"></i>` : ''}
            ${addLinkText}
          </button>
        `);

        $addLink.click(function (e) {
          var $inputContainer = $multiValueContainer
            .children(".multiple-value-group")
            .first();
          // Clone the input container div which contains the input field
          var $clonedInputContainer = $inputContainer.clone();
          // Clear the input field's value and remove the id
          $clonedInputContainer
            .find("> input")
            .val("")
            .removeAttr("id")
            .removeAttr("data-module");

          $clonedInputContainer.addClass("removable-input-container");

          // Append the cloned input container after the last element
          $multiValueContainer.append($clonedInputContainer);

          // Add the 'remove link' to the cloned input container
          module.createRemoveLink($clonedInputContainer);

          var $input = $clonedInputContainer.find("> input");
          var $button = $clonedInputContainer.find("> button");
          $input.outerWidth($multiValueContainer.outerWidth() - $button.outerWidth());

          e.stopPropagation();
          e.preventDefault();
          return false;
        });

        $multiValueContainer.after($addLink);

        if ($multiValueContainer.children(".multiple-value-group").length > 1) {
          $multiValueContainer.children(".multiple-value-group").each(function (subIndex, subElement) {
            if (subIndex > 0) {
              // Add the 'remove link' to all input containers except the first
              $(subElement).addClass("removable-input-container");
              module.createRemoveLink($(subElement));
            }
          });
        }

        $multiValueContainer.data('module-initialized', true);
      });
    },
    createRemoveLink: function (inputContainer) {
      var removeLinkText = this._("Remove");
      // The remove link with the icon
      var removeLink = $(`
        <button type="button" class="btn-link borderless"><i class="far fa-trash"></i>
          ${removeLinkText}
        </button>
      `);
      // Add an event listener for removing the input field container
      removeLink.click(function (e) {
        // Remove the value inside the container's input field
        inputContainer.find("> input").val("");
        // Remove the container
        inputContainer.remove();
        e.stopPropagation();
        e.preventDefault();
        return false;
      });
      // Append the remove link to the input container
      inputContainer.append(removeLink);
      return removeLink;
    }
  };
});
