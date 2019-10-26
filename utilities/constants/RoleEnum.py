
PRODUCT_OWNER = 'PRODUCT_OWNER'
DEVELOPER = 'DEVELOPER'
MANAGER = 'MANAGER'

UserRole = (
    (PRODUCT_OWNER, 'Product Owner'),
    (DEVELOPER, 'Developer'),
    (MANAGER, 'Manager'),
)

# pbi status enum
IN_PROGRESS = 'IN_PROGRESS'
TO_DO = 'TO_DO'
COMPLETED = 'COMPLETED'

PBIStatus = (
    (IN_PROGRESS, 'In Progress'),
    (TO_DO, 'To Do'),
    (COMPLETED, 'Completed')
)


