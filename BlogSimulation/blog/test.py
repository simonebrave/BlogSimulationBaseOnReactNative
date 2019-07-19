from blog.model import createtables, Base

createtables(tables=[Base.metadata.tables['tags'],Base.metadata.tables['blogtags']])