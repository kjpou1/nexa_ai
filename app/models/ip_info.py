from dataclasses import dataclass
from typing import Optional


@dataclass
class IPInfo:
    ip: Optional[str] = None
    hostname: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None

    def __str__(self):
        return (
            f"IP Information:\n"
            f"  IP Address: {self.ip}\n"
            f"  Hostname: {self.hostname}\n"
            f"  City: {self.city}\n"
            f"  Region: {self.region}\n"
            f"  Country: {self.country}\n"
            f"  Latitude: {self.latitude}\n"
            f"  Longitude: {self.longitude}\n"
            f"  Timezone: {self.timezone}\n"
        )
