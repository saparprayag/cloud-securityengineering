#  Checks if MFA is enabled or not

import boto3

iam = boto3.client("iam")
responce = iam.list_users()

for users in responce["Users"]:
    username = users["UserName"]

    # Collect the username name with MFA
    mfa_enabled = iam.list_mfa_devices(UserName=username)
    
    # Checks if MFA is disabled
    if len(mfa_enabled["MFADevices"]) == 0:
        print(f"{username} has no MFA Enabled deactivating the access")

        # collect the access keys of the username
        keys = iam.list_access_keys(UserName=username)
        # Deactivate the access keys or revoke the access keys
        for key in keys["AccessKeyMetadata"]:
            iam.update_access_key(
                UserName=username,
                AccessKeyId=key["AccessKeyId"],
                Status="Inactive")
            
            print(f"Access key deactivated for {username}")
        
        # Removes the console password for the user that has no MFA enabled
        try:
            iam.delete_login_profile(UserName=username)
            print(f"Deleted the login profile for user {username}")
        except:
            print(f"No console password found for user {username}")

    
