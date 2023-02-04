#include "profile.hpp"
#include <string>
#include <vector>

Profile::Profile(std::string user_name, int user_age, std::string user_city, std::string user_country, std::string user_pronouns):name(user_name), age(user_age), city(user_city), country(user_country), pronouns(user_pronouns){}

std::string Profile::view_profile(){
  std::string profile_summary;
  profile_summary = "Hi! My name is "+name+". I live in "+city+" ("+country+"). I am "+std::to_string(age)+" years old and I use "+pronouns+" pronouns.";
  if (hobbies.size()>0){
    profile_summary += "My hobbies are ";
    for (int i=0; i<hobbies.size(); i++){
      if (i<hobbies.size()-2){
        profile_summary += hobbies[i];
        profile_summary += ", ";
      }
      else if (i==hobbies.size()-2){
        profile_summary += hobbies[i];
        profile_summary += " and ";
      }
      else {
        profile_summary += hobbies[i];
        profile_summary += ".";
      }
    }
  }

  return profile_summary;
};

void Profile::add_hobby(std::string new_hobby){
  hobbies.push_back(new_hobby);
}