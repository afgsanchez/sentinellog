from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import LostFoundItem
from .forms import LostFoundItemForm, LostFoundNoteForm
from django.shortcuts import redirect

class LostFoundListView(ListView):
    model = LostFoundItem
    template_name = 'lostfound/lostfound_list.html'
    context_object_name = 'items'
    ordering = ['-found_on']

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        found_by = self.request.GET.get('found_by')
        status = self.request.GET.get('status')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if q:
            qs = qs.filter(description__icontains=q)
        if found_by:
            qs = qs.filter(found_by__icontains=found_by)
        if status:
            qs = qs.filter(status=status)
        if date_from:
            qs = qs.filter(found_on__date__gte=date_from)
        if date_to:
            qs = qs.filter(found_on__date__lte=date_to)
        return qs

class LostFoundDetailView(DetailView):
    model = LostFoundItem
    template_name = 'lostfound/lostfound_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_form'] = LostFoundNoteForm()
        context['notes'] = self.object.notes_list.select_related('created_by').order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = LostFoundNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.item = self.object
            note.created_by = request.user
            note.save()
        return redirect(reverse('lostfound:detail', args=[self.object.pk]))

class LostFoundCreateView(CreateView):
    model = LostFoundItem
    form_class = LostFoundItemForm
    template_name = 'lostfound/lostfound_form.html'
    success_url = reverse_lazy('lostfound:list')

class LostFoundUpdateView(UpdateView):
    model = LostFoundItem
    form_class = LostFoundItemForm
    template_name = 'lostfound/lostfound_form.html'
    success_url = reverse_lazy('lostfound:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_form'] = LostFoundNoteForm()
        context['notes'] = self.object.notes_list.select_related('created_by').order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'save_object' in request.POST:
            return super().post(request, *args, **kwargs)
        elif 'add_note' in request.POST:
            form = LostFoundNoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.item = self.object
                note.created_by = request.user
                note.save()
            return redirect(reverse('lostfound:edit', args=[self.object.pk]))