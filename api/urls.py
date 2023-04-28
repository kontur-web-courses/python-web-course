from rest_framework import routers

from api.views import EmployeesViewSet, OrganizationsViewSet

app_name = "api"

router = routers.SimpleRouter()

router.register(r"organizations", OrganizationsViewSet, basename="organization")
router.register(r"employees", EmployeesViewSet, basename="employee")

urlpatterns = router.urls
