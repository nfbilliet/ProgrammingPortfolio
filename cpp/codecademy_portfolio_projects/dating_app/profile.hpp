#include <iostream>
#include <string>
#include <vector>

class Profile {
  private:
    std::string name;
    int age;
    std::string city;
    std::string country;
    std::string pronouns;
    std::vector<std::string> hobbies; 

  public:
    // Constructor for the Profile class
    Profile(std::string user_name, int user_age, std::string city, std::string country, std::string pronouns);
    std::string view_profile();
    void add_hobby(std::string new_hobby);
};