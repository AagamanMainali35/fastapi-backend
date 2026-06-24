import sys

from app.core.security import hash_password, verify_password

hashed = "$argon2id$v=19$m=65536,t=3,p=4$x7oRIE8GHxRYkDKXFEJvwg$IPko2amSu4YFcNx2Yl+tqjsrFz+9LivQ5j19/rnnVag"

print("New hash:", hash_password("password"))
