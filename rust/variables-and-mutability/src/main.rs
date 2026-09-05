type Meters = i32; // Type aliases allow you to create a new name for an existing type, improving code readability.
const DUBAI_GOAL: bool = true; // With `const`, you must explicitly specify the variable's type.
const TOUCHDOWN_POINTS: i32 = 6;

#[allow(unused_variables)] // This attribute suppresses warnings for unused variables in the following function.
fn main() {
    let age = 32;

    let fruit = 300; // Prefix an unused variable name with an underscore (`_`) to avoid unused-variable warnings.

    println!(
        "My age is {0}, and i am ready to be a awesome DAD! for my child.",
        age
    ); // In Rust's `println!` macro, positional arguments are explicitly indexed starting from `0`.

    let x = "5";
    let x = 5; // Variable shadowing allows you to redeclare a variable with the same name and assign it a new value.

    {
        let age = 31;
        println!("{}", age)
    }

    if DUBAI_GOAL {
        println!("I will achieve my goal in Dubai!");
    }

    let mile_rage_length: Meters = 1600;

    println!("The length of a mile in meters is: {}", mile_rage_length);

    // Section 01 Task
    let season: &str = "Mansoon";
    #[allow(unused_assignments)]
    let mut points_scored: i32 = 28;
    points_scored = 35;
    let event_time = "06:00";
    let event_time = 6;
    let favorite_beverage: &str = "Coffee";

    println!(
        "In the {} season, I scored {} points at {} o'clock.",
        season, points_scored, event_time
    );
    println!("A touchdown is worth {0} points.", TOUCHDOWN_POINTS);
}
