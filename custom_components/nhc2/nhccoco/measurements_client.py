"""REST API client for NHC2 measurements."""
import logging
import aiohttp
import ssl
from datetime import datetime
from typing import Optional, List, Dict, Any

_LOGGER = logging.getLogger(__name__)


class MeasurementsClient:
    """Client for retrieving measurements from NHC2 REST API."""

    def __init__(self, host: str, token: str, port: int = 443, ssl_context: Optional[ssl.SSLContext] = None):
        self._host = host
        self._token = token
        self._port = port
        self._base_url = f"https://{host}:{port}/measurements/v1"
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Use provided SSL context or create a basic one (cert loading done externally)
        if ssl_context:
            self._ssl_context = ssl_context
        else:
            # Create minimal SSL context without loading certificates
            # Certificates should be loaded by the caller to avoid blocking I/O
            self._ssl_context = ssl.create_default_context()
            self._ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

    def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session with increased buffer size for large responses."""
        if self._session is None or self._session.closed:
            # Create connector with larger read buffer to handle large JSON responses
            connector = aiohttp.TCPConnector(limit=10)
            timeout = aiohttp.ClientTimeout(total=60, connect=10, sock_read=30)
            
            self._session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self._token}',
                    'Content-Type': 'application/json'
                },
                connector=connector,
                timeout=timeout,
                # Increase max line size and field size for large JSON responses
                read_bufsize=1024 * 1024  # 1MB buffer instead of default 64KB
            )
        return self._session

    async def close(self):
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()

    def _filter_measurement_values(self, values: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not isinstance(values, list):
            return []

        filtered_values = []
        for value in values:
            if not (isinstance(value, dict) and 
                    "DateTime" in value and 
                    "Value" in value and 
                    value["Value"] is not None):
                continue
            try:
                # Ensure the value can be converted to float
                float(value["Value"])
                filtered_values.append(value)
            except (ValueError, TypeError):
                _LOGGER.debug(f"Filtering out non-numeric measurement entry: {value}")

        return filtered_values

    def _process_successful_response(self, data: bytes, device_uuid: str, property_name: str, interval: str) -> Optional[Dict[str, Any]]:
        try:
            _LOGGER.debug(f"Aggregated measurements response size: {len(data)} bytes")
            
            # Decode and parse JSON manually
            import json
            parsed_data = json.loads(data.decode('utf-8'))
            
            # Filter out invalid values
            if "Values" in parsed_data:
                filtered_values = self._filter_measurement_values(parsed_data["Values"])
                _LOGGER.debug(f"Filtered out {len(parsed_data['Values']) - len(filtered_values)} invalid measurement entries")
                _LOGGER.debug(f"Remaining valid entries: {filtered_values}")
                parsed_data["Values"] = filtered_values
                _LOGGER.debug(f"Filtered {len(filtered_values)} valid measurement entries")
            
            return parsed_data
        except Exception as json_error:
            _LOGGER.error(
                f"Failed to parse JSON response for {device_uuid}/{property_name}/{interval}. "
                f"Response length: {len(data)} bytes, Error: {json_error}"
            )
            return None

    async def _handle_error_response(self, response, device_uuid: str, property_name: str) -> None:
        if response.status == 404:
            _LOGGER.debug(f"Property {property_name} not found for device {device_uuid}")
        else:
            text = await response.text()
            _LOGGER.warning(
                f"Failed to get aggregated measurements for "
                f"{device_uuid}/{property_name}: HTTP {response.status}, Response: {text[:500]}"
            )

    def _format_datetime_for_api(self, dt: datetime) -> str:
        return dt.isoformat()

    async def get_aggregated_measurements(
        self,
        device_uuid: str,
        property_name: str,
        interval: str,
        interval_start: datetime,
        interval_end: datetime,
        aggregation: str = "sum"
    ) -> Optional[Dict[str, Any]]:
        url = f"{self._base_url}/devices/{device_uuid}/properties/{property_name}/{interval}"
        params = {
            "IntervalStart": self._format_datetime_for_api(interval_start),
            "IntervalEnd": self._format_datetime_for_api(interval_end),
            "Aggregation": aggregation
        }
        _LOGGER.debug(f"Requesting aggregated measurements with params: {params}")
        try:
            session = self._get_session()
            async with session.get(url, params=params, ssl=self._ssl_context) as response:
                if response.status == 200:
                    data = await response.read()
                    return self._process_successful_response(data, device_uuid, property_name, interval)
                else:
                    await self._handle_error_response(response, device_uuid, property_name)
                    return None
        except aiohttp.ClientError as e:
            _LOGGER.error(
                f"Error getting aggregated measurements for "
                f"{device_uuid}/{property_name}: {e}"
            )
            return None
