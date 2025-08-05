from typing import Dict, Any, Optional

class GradingService:
    """Service for calculating surf quality grades"""
    
    @staticmethod
    def get_wave_quality(
        wind_direction: float,
        wind_speed: float,
        swell_period: float,
        beach_orientation: float,
        wave_height: float
    ) -> str:
        """
        Calculate surf quality grade based on wave conditions
        
        Args:
            wind_direction: Wind direction in degrees
            wind_speed: Wind speed in knots
            swell_period: Swell period in seconds
            beach_orientation: Beach angle/orientation in degrees
            wave_height: Wave height in feet
            
        Returns:
            str: 'red', 'yellow', or 'green' grade
        """
        score = 0
        
        # Boolean check for unrideable waves
        if wave_height < 1:
            return 'red'
        
        # Normalize wind direction relative to beach orientation
        adjusted_wind_direction = (wind_direction - beach_orientation + 360) % 360
        
        # Determine wind effect on surf quality
        wind_effect = 0
        if 240 <= adjusted_wind_direction <= 300:
            wind_effect = 2  # Offshore wind - beneficial
        elif 60 <= adjusted_wind_direction <= 120:
            wind_effect = -2  # Onshore wind - detrimental
        else:
            wind_effect = -1  # Cross-shore wind - slightly negative
        
        # Adjust wind effect based on wind speed multiplier
        wind_speed_multiplier = 1
        if wind_speed <= 5:
            wind_speed_multiplier = 1.2  # Light wind - positive effect
        elif wind_speed > 15:
            wind_speed_multiplier = 0.5  # Strong wind - negative effect
        
        score += wind_effect * wind_speed_multiplier
        
        # Swell period impact
        if swell_period >= 10:
            score += 2  # Long period - better waves
        elif swell_period < 7:
            score -= 2  # Short period - choppier waves
        
        # Assign final quality grade
        if score >= 4:
            return 'green'
        elif score >= 0:
            return 'yellow'
        else:
            return 'red'
    
    @staticmethod
    def calculate_grade_from_data(
        wind_data: Dict[str, Any],
        wave_data: Dict[str, Any],
        beach_orientation: float
    ) -> Optional[str]:
        """
        Calculate grade from weather data
        
        Args:
            wind_data: Wind data from API
            wave_data: Wave data from API
            beach_orientation: Beach angle in degrees
            
        Returns:
            str: Grade or None if insufficient data
        """
        try:
            # Extract current conditions (first hour of data)
            if 'hourly' not in wind_data or 'hourly' not in wave_data:
                return None
            
            # Get current wind conditions
            wind_speed = wind_data['hourly']['wind_speed_10m'][0]
            wind_direction = wind_data['hourly']['wind_direction_10m'][0]
            
            # Get current wave conditions
            wave_height = wave_data['hourly']['wave_height'][0]
            swell_period = wave_data['hourly']['wave_period'][0]
            
            return GradingService.get_wave_quality(
                wind_direction=wind_direction,
                wind_speed=wind_speed,
                swell_period=swell_period,
                beach_orientation=beach_orientation,
                wave_height=wave_height
            )
            
        except (KeyError, IndexError, TypeError):
            # Return None if we can't extract the required data
            return None 