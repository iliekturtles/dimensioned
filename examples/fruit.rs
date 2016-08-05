extern crate typenum;
#[macro_use]
extern crate dimensioned;

use std::ops::{Add, Div, Mul, Neg, Sub};
use std::marker::{PhantomData};

make_units!{
    Fruit, Unitless, one;
    base {
        Apple, apple, a;
        Banana, banana, b;
        Cucumber, cuke, c;
        Mango, mango, m;
        Watermelon, watermelon, w;
    }
    derived {
    }
}

fn main() {
    let fruit_salad = apple * banana * mango * mango * watermelon;
    // prints "Mmmm, delicious: 1 a*b*m^2*w":
    //println!("Mmmm, delicious: {}", fruit_salad);
}
