# RREL

Here, we present some aspects found in our unittests, which we
think represent typical scoping use cases.

The example is a self-running demo which "interprets" the DSL:
modelled DSL-calls to DSL-methods of DSL-objects are printed...

## Use Cases

 * **global full qualified name lookup** (`Cls.extends=[Cls|FQN]`)
 * **relative/local lookup** (`Call.method` depends on `Call.obj`).
   This might take the **extension of classes within the DSL**
   into account (`Cls.extends`) or not (two use cases).
 * The entire example **consists of two meta models**: one 
   for the class definition and one for the object instances
   and the calls of methods. The **model is distributed among 
   multiple model files**.

## Grammars 

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

and

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

## Non-RREL implementation

using built-in scope providers

    mm_program_supporting_inheritance.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI(),
        "Call.method": scoping_providers.ExtRelativeName("obj.ref",
                                                         "methods",
                                                         "extends")
    })


## RREL implementation

FQN for Classes (one line for each grammar, respectively)
    
    Obj.ref: ^pkg*.cls
    Cls.extends: ^pkg*.cls
 
 and

    Model:
        imports*=Import
        obj*=Obj
        call*=Call;
    
    Obj: "obj" name=ID ":" ref=[Cls|FQN];
    Call: "call"
            obj=[Obj] 
            "."
            method=[Method|ID|~obj.~ref.~methods, ~obj.~ref.~extension*.~methods];
    
    Import: 'import' importURI=STRING;
    Comment: /\/\/.*/;    
    FQN: ID('.'ID)*;

Open: multifile/importURI support
