from django.contrib.auth.models import Group,Permission

def create_groups_permissions(sender,**kwargs):
    
    try:
        #create groups
        readers_group,created = Group.objects.get_or_create(name="Readers")
        authers_group,created = Group.objects.get_or_create(name="Authers")
        editors_group,created = Group.objects.get_or_create(name="Editors")
        
        #create permissions
        readers_permissions =[
            Permission.objects.get(codename='view_post')  
        ]
        
        authers_permissions =[
            Permission.objects.get(codename='add_post'),
            Permission.objects.get(codename='change_post'),
            Permission.objects.get(codename='delete_post'),
            Permission.objects.get(codename='view_post')
        ]
        
        can_publish,created = Permission.objects.get_or_create(codename='can_publish',content_type_id=7,name='Can Publish Post')
        
        editors_permissions =[
            can_publish,
            Permission.objects.get(codename='add_post'),
            Permission.objects.get(codename='change_post'),
            Permission.objects.get(codename='delete_post'),
            Permission.objects.get(codename='view_post')
        ]
        
        
        #assigning the permissions to groups
        readers_group.permissions.set(readers_permissions)
        authers_group.permissions.set(authers_permissions)
        editors_group.permissions.set(editors_permissions)
        
        print("Groups and Permissions created Successfully.")
        
    except Exception as e: 
        print(f'An error occured {e}')
    
    
    
    
    
    
    