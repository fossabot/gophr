from nested_admin.formsets import NestedInlineFormSet

class ComponentFormset(NestedInlineFormSet):

    def __init__(self, *args, **kwargs):

        super(ComponentFormset, self).__init__(*args, **kwargs)
