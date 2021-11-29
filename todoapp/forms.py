# from django import forms
#
# from .models import ToDoList
#
#
# class TodoEditForm(forms.ModelForm):
#     class Meta:
#         model = ToDoList
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(TodoEditForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
