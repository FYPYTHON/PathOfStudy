
import uuid
u_n = uuid.getnode()
var = uuid.UUID(int=u_n).hex[-12:]
print(var)


