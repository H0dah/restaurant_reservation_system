from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class LoginSerializer(serializers.Serializer):
    employee_number = serializers.IntegerField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        employee_number = data.get('employee_number')
        password = data.get('password')

        if employee_number and password:
            try:
                account_obj = Account.objects.get(
                    employee_number=employee_number)
                if not account_obj.user.check_password(password):
                    raise serializers.ValidationError("Incorrect credentials")
                data['user'] = account_obj.user
            except Account.DoesNotExist:
                raise serializers.ValidationError(
                    "This employee number is not registered")
        else:
            raise serializers.ValidationError("Missing credentials")
        return data

    def save(self):
        account = Account.objects.get(
            employee_number=self.validated_data['employee_number'])
        refresh = RefreshToken.for_user(account.user)
        return {
            'user': account.user,
            'token': str(refresh.access_token)
        }
