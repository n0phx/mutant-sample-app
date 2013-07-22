from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mutant import models

from mutantgui.forms import AddFieldForm, get_field_def_form
from mutantgui.utils import get_mutant_type


class TableListView(ListView):
    model = models.ModelDefinition
    context_object_name = 'table_list'
    template_name = 'mutantgui/table_list.html'


list_tables = TableListView.as_view()


class TableCreateView(CreateView):
    model = models.ModelDefinition
    template_name = 'mutantgui/table_save.html'
    success_url = reverse_lazy('table_list')


create_table = TableCreateView.as_view()


class TableUpdateView(UpdateView):
    model = models.ModelDefinition
    template_name = 'mutantgui/table_save.html'
    success_url = reverse_lazy('table_list')


update_table = TableUpdateView.as_view()


class TableDeleteView(DeleteView):
    model = models.ModelDefinition
    template_name = 'mutantgui/table_delete.html'
    success_url = reverse_lazy('table_list')


delete_table = TableDeleteView.as_view()


class FieldListView(ListView):
    model = models.FieldDefinition
    context_object_name = 'field_list'
    template_name = 'mutantgui/field_list.html'

    def get_queryset(self):
        table_pk = self.kwargs.get('table_pk', None)
        return self.model.objects.filter(model_def_id=table_pk)

    def get_context_data(self, **kwargs):
        context = super(FieldListView, self).get_context_data(**kwargs)
        table_pk = self.kwargs.get('table_pk', None)
        try:
            parent_table = models.ModelDefinition.objects.get(pk=table_pk)
        except models.ModelDefinition.DoesNotExist:
            pass
        else:
            context['parent_table_name'] = parent_table.name

        context['parent_table_id'] = table_pk
        context['field_type_form'] = AddFieldForm()

        return context


list_fields = FieldListView.as_view()


class SuccessUrlMixin(object):

    def get_reversed_success_url(self):
        try:
            table_pk = self.kwargs['table_pk']
        except KeyError:
            return reverse('table_list')
        else:
            return reverse('field_list', kwargs={'table_pk': table_pk})


class FieldCreateView(SuccessUrlMixin, CreateView):
    template_name = 'mutantgui/field_save.html'

    def get_success_url(self):
        self.success_url = self.get_reversed_success_url()
        return super(FieldCreateView, self).get_success_url()

    def _prepare_dynamic_form(self, request, table_pk, super_func):
        form = AddFieldForm(request.GET)
        if form.is_valid():
            field_type_pk = form.cleaned_data['field_type']

            table_pk = self.kwargs.get('table_pk', None)
            model_defs = models.ModelDefinition.objects.filter(pk=table_pk)

            self.form_class = get_field_def_form(field_type_pk, model_defs)
            self.model = get_mutant_type(field_type_pk)
            self.initial = {'model_def': table_pk,
                            'content_type': field_type_pk}
            return super_func()
        else:
            return redirect(self.get_success_url())

    def get(self, request, table_pk):
        super_func = lambda: super(FieldCreateView, self).get(request,
                                                              table_pk)
        return self._prepare_dynamic_form(request, table_pk, super_func)

    def post(self, request, table_pk):
        super_func = lambda: super(FieldCreateView, self).post(request,
                                                               table_pk)
        return self._prepare_dynamic_form(request, table_pk, super_func)


create_field = FieldCreateView.as_view()


class FieldUpdateView(SuccessUrlMixin, UpdateView):
    template_name = 'mutantgui/field_save.html'

    def get_success_url(self):
        self.success_url = self.get_reversed_success_url()
        return super(FieldUpdateView, self).get_success_url()

    def get_object(self):
        table_pk = self.kwargs.get('table_pk', None)
        model_defs = models.ModelDefinition.objects.filter(pk=table_pk)

        field_pk = self.kwargs.get('field_pk', None)
        base_field = get_object_or_404(models.FieldDefinition, pk=field_pk)
        field_type_pk = base_field.type_cast().get_content_type().pk

        self.form_class = get_field_def_form(field_type_pk, model_defs)
        self.model = get_mutant_type(field_type_pk)

        field = self.model.objects.get(pk=field_pk)

        return field


update_field = FieldUpdateView.as_view()


class FieldDeleteView(SuccessUrlMixin, DeleteView):
    model = models.FieldDefinition
    template_name = 'mutantgui/field_delete.html'

    def delete(self, *args, **kwargs):
        self.success_url = self.get_reversed_success_url()
        return super(FieldDeleteView, self).delete(*args, **kwargs)


delete_field = FieldDeleteView.as_view()
