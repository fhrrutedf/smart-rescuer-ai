"""
Emergency Dispatcher
Sends reports to EMS services
"""
from typing import Dict, Any, Optional
import requests
from utils import log, config


class EmergencyDispatcher:
    """Send emergency reports to EMS"""
    
    def __init__(self, api_endpoint: str = None, api_key: str = None):
        """
        Initialize dispatcher
        
        Args:
            api_endpoint: EMS API endpoint
            api_key: API authentication key
        """
        self.api_endpoint = api_endpoint or config.EMS_API_ENDPOINT
        self.api_key = api_key or config.EMS_API_KEY
        self.enabled = bool(self.api_endpoint and self.api_key)
        
        if not self.enabled:
            log.warning("EMS dispatcher not configured - reports will be saved locally only")
        else:
            log.info(f"EMS dispatcher initialized (endpoint: {self.api_endpoint})")
    
    def dispatch_report(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send report to EMS
        
        Args:
            report: Emergency report from ReportGenerator
            
        Returns:
            Dispatch result with status
        """
        if not self.enabled:
            log.info("EMS dispatch skipped (not configured)")
            return {
                "status": "not_sent",
                "reason": "EMS API not configured",
                "local_only": True
            }
        
        try:
            log.info(f"Dispatching report {report.get('report_id')} to EMS...")
            
            # Prepare request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": f"SmartRescuer/{config.APP_VERSION}"
            }
            
            # Send report
            response = requests.post(
                self.api_endpoint,
                json=report,
                headers=headers,
                timeout=10
            )
            
            # Check response
            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                log.info(f"Report dispatched successfully: {result}")
                return {
                    "status": "sent",
                    "ems_response": result,
                    "status_code": response.status_code
                }
            else:
                log.error(f"EMS dispatch failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "error": f"HTTP {response.status_code}",
                    "details": response.text
                }
                
        except requests.ConnectionError:
            log.error("EMS dispatch failed: Connection error (no internet?)")
            return {
                "status": "failed",
                "error": "connection_error",
                "local_only": True
            }
        except requests.Timeout:
            log.error("EMS dispatch failed: Request timeout")
            return {
                "status": "failed",
                "error": "timeout"
            }
        except Exception as e:
            log.error(f"EMS dispatch failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def send_location_update(self, location: Dict[str, Any], report_id: str) -> bool:
        """
        Send location update for ongoing emergency
        
        Args:
            location: GPS location data
            report_id: Original report ID
            
        Returns:
            True if successful
        """
        if not self.enabled:
            return False
        
        try:
            update_endpoint = f"{self.api_endpoint}/location"
            
            payload = {
                "report_id": report_id,
                "location": location,
                "timestamp": location.get("timestamp")
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.post(
                update_endpoint,
                json=payload,
                headers=headers,
                timeout=5
            )
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            log.error(f"Location update failed: {e}")
            return False
