from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import SpeedLevel
from django.db.models import Sum
from .serilaizers import SpeedSerializers
from django.utils.timezone import make_aware, is_naive
# Create your views here.

voltage = 220
power_factor = 0.8

def dummy_template_view(request):
    return render(request, "power/dummy_template.html")


class SpeedCreateAPIview(APIView):
    @staticmethod
    def post(request):
        serialiers_data = SpeedSerializers(data=request.data)
        if serialiers_data.is_valid():
            serialiers_data.save()
            return Response(serialiers_data.data, status=status.HTTP_200_OK)
        
        return Response(serialiers_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get(request):
        data = SpeedSerializers(SpeedLevel.objects.all(), many=True).data
        return Response({"data": data}, status=status.HTTP_200_OK)



class EnergyConsumerAPIview(APIView):
    @staticmethod
    def post(request):
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")

        if not start_time or not end_time:
            return Response({"error": "start_time and end_time are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)

            if is_naive(start_time):
                start_time = make_aware(start_time)
            if is_naive(end_time):
                end_time = make_aware(end_time)
        except ValueError:
            return Response({"error": "Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)."}, status=status.HTTP_400_BAD_REQUEST)

        records = SpeedLevel.objects.filter(start_time__lt=end_time).order_by("start_time")

        if not records.exists():
            return Response({"message": "No data found for the specified time range."}, status=status.HTTP_404_NOT_FOUND)

        total_energy = 0 
        if records.first().start_time < start_time:
            first_record = records.first()
            current_amperage = first_record.speed
            time_duration = (records[1].start_time - start_time).total_seconds() / 3600 
            power = current_amperage * voltage * power_factor
            total_energy += power * time_duration

        for i in range(1, len(records) - 1):
            current_record = records[i]
            next_record = records[i + 1]
            current_amperage = current_record.speed
            time_duration = (next_record.start_time - current_record.start_time).total_seconds() / 3600  
            power = current_amperage * voltage * power_factor
            total_energy += power * time_duration

        last_record = records.last()
        current_amperage = last_record.speed
        if last_record.start_time < end_time:
            time_duration = (end_time - max(last_record.start_time, start_time)).total_seconds() / 3600  
            power = current_amperage * voltage * power_factor
            total_energy += power * time_duration


        return Response({
            "total_energy": round(total_energy, 2) 
        }, status=status.HTTP_200_OK)