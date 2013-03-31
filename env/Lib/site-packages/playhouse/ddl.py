from peewee import *
# lower-level
class BaseDDL(object):
    def __sql__(self):
        return str(self)

class Clause(BaseDDL):
    """
    A single or compound clause, for example ``CREATE TABLE`` -- in some cases
    clauses make take parameters, e.g. ``VARCHAR(255)``
    """
    __slots__ = ['name', 'params']

    def __init__(self, name, *params):
        self.name = name
        self.params = params

    def __call__(self, *args):
        return Clause(self.name, *args)

class QuotedName(BaseDDL):
    """
    A quoted name, for example a table or column name
    """
    __slots__ = ['name', 'quote_char']

    def __init__(self, name, quote_char='"'):
        self.name = name
        self.quote_char = quote_char

class ClauseGroup(BaseDDL):
    """
    One or more clauses logically grouped.  When parsed, each clause will be
    separated by a single space
    """
    __slots__ = ['clauses']

    def __init__(self, *args):
        self.clauses = list(args)

class ClauseList(ClauseGroup):
    """
    One or more clauses to render inside parentheses separated by commas
    """
    pass

class DDLConstruct(object):
    pass

# high level abstractions
class DDLField(DDLConstruct):
    __slots__ = ['field']

    def __init__(self, field):
        self.field = field

    def __ddl__(self, compiler):
        field_type = self.field.get_column_type()
        return ClauseGroup(
            QuotedName(self.field.db_column),
            Clause(
                compiler.fields[field_type],
                *self.field.get_column_args()
            )
        )

class DDLTable(DDLConstruct):
    def __init__(self, model_class):
        self.model_class = model_class

    def __ddl__(self, compiler):
        meta = self.model_class._meta
        field_ddl = [DDLField(f) for f in meta.get_fields()]
        return ClauseGroup(
            Clause('CREATE TABLE'),
            QuotedName(meta.db_table),
            ClauseList(*field_ddl),
        )


class DDLCompiler(object):
    def __init__(self, quote_char='"'):
        self.quote_char = quote_char

    def parse(self, atom):
        if isinstance(atom, Clause):
            sql = atom.name
            if atom.params:
                parsed_params = map(self.parse, atom.params)
                sql += '(%s)' % ', '.join(map(self.parse, atom.params))
            return sql
        elif isinstance(atom, QuotedName):
            return atom.name.join((self.quote_char, self.quote_char))
        elif isinstance(atom, FieldResolver):
            pass
        elif isinstance(atom, ClauseList):
            return '(%s)' % ', '.join(map(self.parse, atom.clauses))
        elif isinstance(atom, ClauseGroup):
            return ' '.join(map(self.parse, atom.clauses))
        return str(atom)

    def parse_list(self, *atoms):
        return self.parse(ClauseGroup(*atoms))

compiler = DDLCompiler()
"""
DDL... how is it organized

CREATE <TEMP> TABLE <IF NOT EXISTS> `tblname` ...
    ( coldefs, table constraint )
    AS <select stmt>

coldef:
    `colname` COLTYPE (col constraints)

COLTYPE: name(xxxx)

CONSTRAINT <name>
PRIMARY KEY (ASC/DESC) AUTOINCREMENT
NOT NULL
UNIQUE
CHECK (expr)
DEFAULT [signed / literal / expr]
COLLATE <name>

FK:

REFERENCES `table` (`colz`)

ON [delete/update] SET NULL/DEFAULT ... CASCADE ... RESTRICT ...
[NOT] DEFERRABLE [INITIALLY DEFERRED/IMMEDIATE]
"""

