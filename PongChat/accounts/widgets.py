from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    """Custom file input widget.

    This widget customizes the file input field to remove the default
    display of the current file path and clear checkbox.

    Attributes:
        template_name (str): The template used for rendering the widget.
    """

    template_name = "custom_widgets/custom_clearable_file_input.html"
