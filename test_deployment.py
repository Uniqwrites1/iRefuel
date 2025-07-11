#!/usr/bin/env python3
"""
Quick test script to verify the Render deployment status
"""

import requests
import json

def test_render_deployment():
    """Test the Render deployment endpoints"""
    
    base_url = "https://irefuel.onrender.com"
    
    print("🧪 Testing University Vendor App Deployment")
    print("=" * 50)
    
    # Test endpoints
    endpoints = [
        "/",
        "/api/",
        "/api/health/",
        "/admin/",
        "/api/auth/register/",
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\n📍 Testing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 400 and "ALLOWED_HOSTS" in response.text:
                print("   ⚠️  ALLOWED_HOSTS error detected!")
                print("   🔧 Fix needed: Update ALLOWED_HOSTS environment variable")
            elif response.status_code in [200, 201, 301, 302]:
                print("   ✅ Endpoint responding correctly")
            else:
                print(f"   ❓ Response: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Next Step: Update ALLOWED_HOSTS in Render dashboard")
    print("   Variable: ALLOWED_HOSTS")
    print("   Value: irefuel.onrender.com")

if __name__ == "__main__":
    test_render_deployment()
