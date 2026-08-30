fn main() {
    let age = 32;

    let _fruit = 300; // Prefix an unused variable name with an underscore (`_`) to avoid unused-variable warnings.

    println!(
        "My age is {0}, and i am ready to be a awesome DAD! for my child.",
        age
    ); // In Rust's `println!` macro, positional arguments are explicitly indexed starting from `0`.

    let _x = "5";
    let _x = 5; // Variable shadowing allows you to redeclare a variable with the same name and assign it a new value.

    {
        let age = 31;
        println!("{}", age)
    }
}
