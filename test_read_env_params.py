import os

# for k, v in os.environ.items():
#     print(k,':', v)
#     print('------------------------------------------------')

print(list(os.environ.get('LC_MEASUREMENT')))
