extern crate typenum;
#[macro_use]
extern crate dimensioned;

use std::ops::{Add, Div, Mul, Neg, Sub};
use std::marker::{PhantomData};

make_units! {
    Fruit, Unitless, one;
    base {
        Apple, apple, A;
        Banana, banana, B;
        Cucumber, cucumber, C;
    }
    derived {
    }
}


#[test]
fn test_making_units() {
    let x = apple;
    //println!("{}", x*2.0*x);
}
