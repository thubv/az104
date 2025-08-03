#!/usr/bin/env python3
"""
Retry failed units from the batch crawl
"""

import asyncio
import json
from pathlib import Path
from az104_image_crawler import AZ104ImageCrawler

class FailedUnitsRetry:
    """Retry failed units with enhanced error handling"""
    
    def __init__(self):
        self.crawler = AZ104ImageCrawler()
        self.course_structure_file = Path("content/course_structure.json")
        
        # List of failed units from the batch crawl log
        self.failed_units = [
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/create-azure-resource-manager-template-vs-code/5-exercise-parameters-output/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az104-admin-prerequisites",
                "path": "content/english/01_AZ-104-_Prerequisites_for_Azure_administrators/05_Create_Azure_Resource_Manager_Template_Vs_Code/05_Exercise_-_Add_parameters_and_outputs_to_your_Azure_Resource_Manager_template.html",
                "title": "Exercise - Add parameters and outputs to your Azure Resource Manager template"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/create-configure-manage-identities/3-exercise-assign-licenses-users/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-identities-governance",
                "path": "content/english/02_AZ-104-_Manage_identities_and_governance_in_Azure/02_Create_Configure_Manage_Identities/03_Exercise_-_assign_licenses_to_users.html",
                "title": "Exercise - assign licenses to users"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/create-configure-manage-identities/9-exercise-change-group-license-assignments/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-identities-governance",
                "path": "content/english/02_AZ-104-_Manage_identities_and_governance_in_Azure/02_Create_Configure_Manage_Identities/09_Exercise_-_change_group_license_assignments.html",
                "title": "Exercise - change group license assignments"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/create-configure-manage-identities/10-exercise-change-user-license-assignments/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-identities-governance",
                "path": "content/english/02_AZ-104-_Manage_identities_and_governance_in_Azure/02_Create_Configure_Manage_Identities/10_Exercise_-_change_user_license_assignments.html",
                "title": "Exercise - change user license assignments"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/3-get-started-azure-accounts/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-identities-governance",
                "path": "content/english/02_AZ-104-_Manage_identities_and_governance_in_Azure/03_Describe_Core_Architectural_Components_Of_Azure/03_Get_started_with_Azure_accounts.html",
                "title": "Get started with Azure accounts"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/sovereignty-policy-initiatives/azure-policy-resources/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-identities-governance",
                "path": "content/english/02_AZ-104-_Manage_identities_and_governance_in_Azure/04_Sovereignty_Policy_Initiatives/04_Azure_Policy_resources.html",
                "title": "Azure Policy resources"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/4-list-access/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-identities-governance",
                "path": "content/english/02_AZ-104-_Manage_identities_and_governance_in_Azure/05_Secure_Azure_Resources_With_Rbac/04_Exercise_-_List_access_using_Azure_RBAC_and_the_Azure_portal.html",
                "title": "Exercise - List access using Azure RBAC and the Azure portal"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/configure-vnet-peering/3-determine-gateway-transit-connectivity/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-virtual-networks",
                "path": "content/english/03_AZ-104-_Configure_and_manage_virtual_networks/04_Configure_Vnet_Peering/03_Determine_gateway_transit_and_connectivity.html",
                "title": "Determine gateway transit and connectivity"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/configure-vnet-peering/6-simulation-peering/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-virtual-networks",
                "path": "content/english/03_AZ-104-_Configure_and_manage_virtual_networks/04_Configure_Vnet_Peering/06_Exercise_-_Implement_Intersite_Connectivity.html",
                "title": "Exercise - Implement Intersite Connectivity"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/configure-azure-files-file-sync/5-implement-file-sync/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-storage",
                "path": "content/english/04_AZ-104-_Implement_and_manage_storage_in_Azure/04_Configure_Azure_Files_File_Sync/05_Implement_soft_delete_for_Azure_Files.html",
                "title": "Implement soft delete for Azure Files"
            },
            {
                "url": "https://learn.microsoft.com/en-us/training/modules/configure-azure-app-services/10-use-application-insights/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-compute-resources",
                "path": "content/english/05_AZ-104-_Deploy_and_manage_Azure_compute_resources/04_Configure_Azure_App_Services/10_Use_Azure_Application_Insights.html",
                "title": "Use Azure Application Insights"
            }
        ]
    
    async def retry_failed_units(self):
        """Retry all failed units with enhanced error handling"""
        print("🔄 Retrying failed units with enhanced error handling")
        print("=" * 60)
        
        success_count = 0
        still_failed = []
        
        for i, unit in enumerate(self.failed_units, 1):
            print(f"\n📖 Retrying {i}/{len(self.failed_units)}: {unit['title']}")
            
            try:
                output_path = Path(unit['path'])
                success = await self.crawler.recrawl_single_unit(unit['url'], output_path)
                
                if success:
                    success_count += 1
                    print(f"✅ Success: {unit['title']}")
                else:
                    still_failed.append(unit)
                    print(f"❌ Still failed: {unit['title']}")
                
                # Longer delay between requests
                await asyncio.sleep(10)
                
            except Exception as e:
                still_failed.append(unit)
                print(f"❌ Exception for {unit['title']}: {e}")
                await asyncio.sleep(5)
        
        # Final report
        print(f"\n🎉 Retry completed!")
        print(f"✅ Successfully retried: {success_count}/{len(self.failed_units)} units")
        print(f"❌ Still failed: {len(still_failed)} units")
        
        if still_failed:
            print(f"\n📋 Units still failing:")
            for unit in still_failed:
                print(f"   - {unit['title']}")
        
        await self.crawler.close_session()
        return success_count, still_failed
    
    async def retry_specific_unit(self, unit_url, output_path, title):
        """Retry a specific unit with maximum effort"""
        print(f"🎯 Focused retry: {title}")
        
        # Try multiple times with different strategies
        strategies = [
            {"wait_time": 10000, "retries": 1},
            {"wait_time": 15000, "retries": 2},
            {"wait_time": 20000, "retries": 3}
        ]
        
        for strategy_idx, strategy in enumerate(strategies, 1):
            print(f"🔄 Strategy {strategy_idx}: wait={strategy['wait_time']}ms, retries={strategy['retries']}")
            
            for attempt in range(strategy['retries']):
                try:
                    success = await self.crawler.recrawl_single_unit(unit_url, Path(output_path))
                    if success:
                        print(f"✅ Success with strategy {strategy_idx}, attempt {attempt + 1}")
                        return True
                    
                    await asyncio.sleep(strategy['wait_time'] / 1000)
                    
                except Exception as e:
                    print(f"❌ Strategy {strategy_idx}, attempt {attempt + 1} failed: {e}")
                    await asyncio.sleep(5)
        
        print(f"❌ All strategies failed for: {title}")
        return False

async def main():
    """Main function for retrying failed units"""
    retry_tool = FailedUnitsRetry()
    
    print("AZ-104 Failed Units Retry Tool")
    print("=" * 40)
    print("1. Retry all failed units")
    print("2. Retry specific unit")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        success_count, still_failed = await retry_tool.retry_failed_units()
        
        if still_failed:
            print(f"\n🤔 Would you like to try the remaining {len(still_failed)} units with maximum effort?")
            confirm = input("(y/N): ").strip().lower()
            
            if confirm in ['y', 'yes']:
                print("\n🎯 Trying remaining units with maximum effort...")
                final_success = 0
                for unit in still_failed:
                    success = await retry_tool.retry_specific_unit(
                        unit['url'], 
                        unit['path'], 
                        unit['title']
                    )
                    if success:
                        final_success += 1
                    await asyncio.sleep(15)
                
                print(f"\n🏁 Final results:")
                print(f"✅ Total successful: {success_count + final_success}")
                print(f"❌ Total failed: {len(still_failed) - final_success}")
    
    elif choice == "2":
        print("\nAvailable failed units:")
        for i, unit in enumerate(retry_tool.failed_units, 1):
            print(f"{i}. {unit['title']}")
        
        try:
            unit_idx = int(input(f"\nSelect unit (1-{len(retry_tool.failed_units)}): ")) - 1
            if 0 <= unit_idx < len(retry_tool.failed_units):
                unit = retry_tool.failed_units[unit_idx]
                await retry_tool.retry_specific_unit(unit['url'], unit['path'], unit['title'])
            else:
                print("❌ Invalid selection")
        except ValueError:
            print("❌ Invalid input")
    
    elif choice == "3":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid option selected.")

if __name__ == "__main__":
    asyncio.run(main())