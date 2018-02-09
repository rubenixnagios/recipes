from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from cookbook.forms import EditRecipeForm
from cookbook.models import Recipe, Category


@login_required
def recipe(request, recipe_id):
    recipe_obj = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = EditRecipeForm(request.POST)
        if form.is_valid():
            recipe_obj.name = form.cleaned_data['name']
            recipe_obj.path = form.cleaned_data['path']
            recipe_obj.category = Category.objects.get(name=form.cleaned_data['category'])
            recipe_obj.keywords.clear()
            recipe_obj.keywords.add(*list(form.cleaned_data['keywords']))
            recipe_obj.save()
            messages.add_message(request, messages.SUCCESS, _('Recipe updated'))
            return redirect(reverse_lazy('edit_recipe', args=[recipe_id]))
        else:
            messages.add_message(request, messages.ERROR, _('Recipe update failed'))
    else:
        form = EditRecipeForm(instance=recipe_obj)

    return render(request, 'edit/recipe.html', {'form': form})


@login_required
def category(request, category_id):
    return render(request, 'index.html')


@login_required
def keyword(request, keyword_id):
    return render(request, 'index.html')