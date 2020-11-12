

def print_class_enum(class_Enum) -> int:

    values = []

    print(f"\n** {class_Enum.__name__}:\n".replace("_"," "))

    for key, value in class_Enum.__members__.items():
        print(f" {value.value} <-- {key}".replace("_"," "))
        values.append(value.value)

    value = int(input("\n* What's your choice? "))

    if value not in values:
        raise ValueError("Invalid choice")

    print()  

    return value