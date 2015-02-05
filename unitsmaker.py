#!/usr/bin/env python3

class Units:
    def __init__(self):
        self.name = "Units"
        self.filename = "units.rs"
        self.units = [] # List of names for the units in the type
        self.print_as = [] # Corresponding list of symbols to use for printing
        self.constants = [] # Corresponding list of constants to define
        self.vtype = "f64" # type to define constants for
        self.one = "1.0" # value to set constants to
        self.unitless = "one" # name for the dimensionless constant 1
        self.allowed_root = 1
    def make_units(self):
        if len(self.units) != len(self.print_as) or len(self.units) != len(self.constants):
            print("The lists of units, print_as, and constants must all be the same length.")
            exit(1)
        name = self.name
        ushort = ", ".join(self.units)
        ulong = ", ".join([u + ": PInt" for u in self.units])
        u1_list = [u + "1" for u in self.units]
        u2_list = [u + "2" for u in self.units]
        uboth = ", ".join(u1_list + u2_list)
        u1 = ", ".join(u1_list)
        u2 = ", ".join(u2_list)
        text = """
// This is a generated file. It was created using unitsmaker.py.
#![allow(non_upper_case_globals)]
use peano::*;
use dimensioned::*;

pub struct {name}<{ulong}>;
impl<{ulong}> Dim for {name}<{ushort}> {{}}

""".format(**locals())

        for op in ["Add", "Sub", "Mul"]:
            u1_long = ", ".join([u1+": PInt + {}Peano<{}>".format(op, u2) for (u1, u2) in zip(u1_list, u2_list) ])
            u2_long = ", ".join([u+": PInt" for u in u2_list])
            outs = ", ".join(["<{} as {}Peano<{}>>::Output".format(u1, op, u2) for (u1, u2) in zip(u1_list, u2_list)])
            text += """
impl<{uboth}> {op}Dim<{name}<{u2}>> for {name}<{u1}>
where {u1_long}, {u2_long}
{{
  type Output = {name}<{outs}>;
}}
""".format(**locals())
        root_num = "Zero"
        for i in range(self.allowed_root):
            root_num = "Succ<" + root_num + ">"

        type_sig = ", ".join(["Zero" for u in self.units])
        text += "pub type Unitless = {name}<{type_sig}>;\n".format(**locals())
        text += "impl Dimensionless for Unitless {}\n"
        for i, u in enumerate(self.units):
            type_sig = []
            for j in range(i):
                type_sig += ["Zero"]
            type_sig += [root_num]
            for j in range(i+1, len(self.units)):
                type_sig += ["Zero"]
            type_sig = ", ".join(type_sig)
            text += "pub type {u} = {name}<{type_sig}>;\n".format(**locals())

        vtype = self.vtype
        one = self.one
        text += "\n"
        text += "pub static {}: Dimensioned<Unitless, {}> = Dimensioned({});\n".format(self.unitless, vtype, one)
        for (c, u) in zip(self.constants, self.units):
            text += "pub static {c}: Dimensioned<{u}, {vtype}> = Dimensioned({one});\n".format(**locals())

        f = open(self.filename, "w")
        f.write(text)
        f.close()


def main():
    si = Units()
    si.name = "SI"
    si.filename = "src/si.rs"
    si.units = ["Meter", "Kilogram", "Second", "Amp", "Kelvin", "Candela", "Mole"]
    si.constants = ["m", "kg", "s", "A", "K", "cd", "mol"]
    si.print_as = si.constants
    si.make_units()


if __name__ == "__main__":
    main()