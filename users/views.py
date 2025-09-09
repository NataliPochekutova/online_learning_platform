from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method_payment"]
    ordering_fields = ("data_payment",)


class PaymentCreateAPIView(CreateAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get("course")

        if course_id:
            payment.course = get_object_or_404(Course, pk=course_id)
            product = payment.course.name
        else:
            lesson_id = self.request.data.get("lesson")
            payment.lesson = get_object_or_404(Lesson, pk=lesson_id)
            product = payment.lesson.name

        product_id = PaymentStripe.create_stripe_product(product)
        amount = self.request.data.get("amount_payment")
        price = PaymentStripe.create_stripe_price(product_id, amount)
        session_id, session_url = PaymentStripe.create_stripe_session(price)
        payment.session_id = session_id
        payment.link = session_url
        payment.method_payment = "non_cash"
        payment.save()
