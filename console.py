import cmd
class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb)'
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    def do_EOF(self, arg):
        """Exit the program"""
        return True
    def emptyline(self):
        """Do nothing on empty line"""
        pass

     def do_create(self, arg):
        """Creates a new instance of BaseModel,
        State,City, Amenity, Place,
        /or reviews,save it, and print the id"""

        if not arg:
            print("** class name missing **")
            return

        try:
            # Create an instance of the given class dynamically
            class_name = arg.capitalize()  # Caps the class name
            new_instance = globals()[class_name]()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class doesn't exist **")


        def do_show(self, arg):
        """
            based on the class name and id, prints the string
            representation of an instance of BaseModel,
            State, City, Amenity, Place, Review, or User.
        """
            if not arg:
            print("** class name missing **")
            return

        try:
            args = arg.split()
            class_name = args[0].capitalize()
            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            instance = storage.all().get(key)
            if instance:
                print(instance)
            else:
                print("** no instance found **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** class doesn't exist **")


         def do_destroy(self, arg):
        """
            Based on the class name and id,
            deletes an instance of BaseModel, State, City,
            Amenity, Place, Review, or User.
        """
        if not arg:
            print("** class name missing **")
            return

        try:
            args = arg.split()
            class_name = args[0].capitalize()
            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            instances = storage.all()
            if key in instances:
                del instances[key]
                storage.save()
            else:
                print("** no instance found **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** class doesn't exist **")


         def do_all(self, arg):
        """
            Prints all occurrences of BaseModel, State,
            City, Amenity, Place,
            Review, or User as string representations.
        """
        try:
            class_name = arg.capitalize()
            instances = storage.all()[class_name]
            print(instances)
        except KeyError:
            print("** class doesn't exist **")


        def do_update(self, arg):
            """
                uses the class name and id to update an
                instance of BaseModel, State, City, Amenity,
                Place, Review, or User with a dictionary representation
                (saving the change into the JSON file)
            """
            if not arg:
            print("** class name missing **")
            return

        try:
            args = arg.split()
            class_name = args[0].capitalize()
            instance_id = args[1]
            dictionary_repr = eval(args[2])

            key = "{}.{}".format(class_name, instance_id)
            instances = storage.all()
            if key in instances:
                instance = instances[key]
                for k, v in dictionary_repr.items():
                    setattr(instance, k, v)
                instance.save()
            else:
                print("** no instance found **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
