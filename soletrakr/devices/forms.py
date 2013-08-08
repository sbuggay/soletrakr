from django import forms
from django.contrib.auth.models import User

from devices.models import Device, DeviceManager


class DeviceCreationForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = (
        	'serial_number',
        	'sim_serial_number',
        	'date_manufactured',
        	'phone_number'
        )


    def clean(self):
        """
        Overwritten clean method to validate that the newly created
        device doesn't already exist in the database.
        """
        if Device.objects.filter(serial_number=self.cleaned_data['serial_number']).exists():
            raise forms.ValidationError('Device already exists.')

        return self.cleaned_data


    def save(self):
    	"""
    	Overwritten save method to create new device
    	using the device manager.
    	"""
    	return DeviceManager.create_device (
    		serial_number = self.cleaned_data['serial_number'],
    		sim_serial_number = self.cleaned_data['sim_serial_number'],
    		date_manufactured = self.cleaned_data['date_manufactured'],
    		phone_number = self.cleaned_data['phone_number']
    	)




class DeviceActivationForm(forms.Form):
    """
    Form used to activate previously created devices.
    """
    user = forms.EmailField()
    device = forms.CharField()


    def clean(self):
        """
        Clean function to check for valid user and inactive device
        before attempting the activation process.
        """
        try:
            User.objects.get(email__exact=self.cleaned_data['user'])
        except:
            raise forms.ValidationError('User does not exist.')

        try:
            Device.objects.filter(is_active=False).get(serial_number__exact=self.cleaned_data['device'])
        except:
            raise forms.ValidationError('Device is not available.')

        return self.cleaned_data


    def save(self):
        """
        Save function to activate the given device once the device and user
        info have been validated.
        """
        user = User.objects.get(email__exact=self.cleaned_data['user'])
        device = Device.objects.get(serial_number__exact=self.cleaned_data['device'])

        return DeviceManager.activate_device(device=device, user=user)