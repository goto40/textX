from __future__ import unicode_literals
from textx import metamodel_from_str, get_children_of_type
import textx.scoping.providers as scoping_providers
from textx.scoping import MetaModelProvider
from os.path import dirname, abspath, join

grammar_classes = r'''
Model: 
    imports*=Import
    pkg*=Pkg 
    cls*=Cls;

Pkg: "package" name=ID
    "{"
        pkg*=Pkg
        cls*=Cls
    "}";

Cls: "class" name=ID (
    ( "extends" extends+=[Cls|FQN][','])?
    "{"
        methods+=Method*
    "}"
    )?;

Method: "method" name=ID;

Import: 'import' importURI=STRING;
Comment: /\/\/.*/;
FQN: ID('.'ID)*;
'''

grammer_program = r'''
Model:
    imports*=Import
    obj*=Obj
    call*=Call;

Obj: "obj" name=ID ":" ref=[Cls|FQN];
Call: "call"
        obj=[Obj] 
        "."
        method=[Method];

Import: 'import' importURI=STRING;
Comment: /\/\/.*/;    
FQN: ID('.'ID)*;
'''


def main(debug=False):
    this_folder = dirname(abspath(__file__))

    mm_classes = metamodel_from_str(grammar_classes)
    mm_classes.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI()
    })
    MetaModelProvider.add_metamodel("*.def", mm_classes)

    mm_program_not_supporting_inheritance = metamodel_from_str(
        grammer_program, referenced_metamodels=[mm_classes])

    mm_program_not_supporting_inheritance.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI(),
        "Call.method": scoping_providers.RelativeName("obj.ref.methods")
    })

    mm_program_supporting_inheritance = metamodel_from_str(
        grammer_program, referenced_metamodels=[mm_classes])
    mm_program_supporting_inheritance.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI(),
        "Call.method": scoping_providers.ExtRelativeName("obj.ref",
                                                         "methods",
                                                         "extends")
    })

    prg_full = mm_program_supporting_inheritance.model_from_file(
        join(this_folder, "model", "my_program_full.prg"))
    for call in get_children_of_type("Call", prg_full):
        print("calling {}.{}".format(call.obj.name,
                                     call.method.name))


if __name__ == "__main__":
    main()
