from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.apps import apps


# Create your views here.

def dashboard_home(request):
    # models = apps.get_models()  # will fetch all the models
    # models = apps.get_app_config('app_blogs').get_models() # will fetch the models from a specific application
    context = {}
    context['model_names'] = [model.__name__ for model in apps.get_app_config('app_blogs').get_models()]
    return render(request, "dashboard/dashboard.html", context)


def fetch_models_data(request, model):
    MyModel = apps.get_model(app_label='app_blogs', model_name=model)
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
        "model_names" : [model.__name__ for model in apps.get_app_config('app_blogs').get_models()],
        "fields_name" : general_fields+relational_fields,
        "records" : MyModel.objects.values(*(general_fields+relational_fields)),
        "object" : MyModel,
        "object_name": MyModel.__name__
    }
    return render(request, "dashboard/dashboard_model_views.html", context)