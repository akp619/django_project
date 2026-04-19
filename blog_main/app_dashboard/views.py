from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.apps import apps
from .utils import fetch_models
from django.contrib.auth.models import User

#

# Create your views here.
def dashboard_home(request):
    context = {}
    models = fetch_models(app_name="app_blogs", model_name=False)
    context['models'] = [(model.__name__,model.objects.count()) for model in models] + [(User.Meta.verbose_name_plural, User.objects.count())]
    print("===context===", context)
    return render(request, "dashboard/dashboard.html", context)


def fetch_models_data(request, model):
    if model.lower() == "users":
        MyModel = User
    else:
        MyModel = fetch_models(app_name="app_blogs", model_name=model)
    exclude_fields = ['created', 'updated']
    # field_names = [field.verbose_name for field in MyModel._meta.fields if field.name not in exclude_fields ]
    relational_fields = []
    image_fields = []
    general_fields = []
    model_fields = MyModel._meta.fields
    for field in model_fields:
        if field.is_relation:
            if str(field.related_model).replace("'>","").split('.')[-1] == "User":
                relational_fields.append(f"{field.name}__username")
            else:
                relational_fields.append(f"{field.name}__name")
        elif field.get_internal_type() == "FileField":
            image_fields.append(field)
        elif field.name not in exclude_fields:
            general_fields.append(field.name)
    context = {
        "model_names" : [model.__name__ for model in apps.get_app_config('app_blogs').get_models()] + [(User.Meta.verbose_name_plural)],
        "fields_name" : general_fields+relational_fields,
        "records" : MyModel.objects.values(*(general_fields+relational_fields)),
        "object" : MyModel,
        "object_name": MyModel.__name__
    }
    return render(request, "dashboard/dashboard_model_views.html", context)