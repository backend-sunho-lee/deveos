#include <eosiolib/eosio.hpp>

using namespace eosio;
using namespace std;

class [[eosio::contract]] addressbook : public contract {

private:
  struct [[eosio::table]] person {
    name key;
    string first_name;
    string last_name;
    string street;
    string city;
    uint64_t primary_key() const { return key.value; }
  };
  typedef eosio::multi_index<"people"_n, person> address_index;

public:
  //using contract::contract;
  addressbook(name receiver, name code, datastream<const char*> ds):contract(receiver, code, ds) {}

  [[eosio::action]]
  void upsert(name user, string first_name, string last_name, string street, string city, string state) {
    address_index addresses(_code, _code.value);
    auto iterator = addresses.find(user.value);
    if( iterator == addresses.end() )
    {
      addresses.emplace(user, [&]( auto& row ) {
       row.key = user;
       row.first_name = first_name;
       row.last_name = last_name;
       row.street = street;
       row.city = city;
      });
    }
    else {
      addresses.modify(iterator, user, [&]( auto& row ) {
        row.key = user;
        row.first_name = first_name;
        row.last_name = last_name;
        row.street = street;
        row.city = city;
      });
    }
  }

};

EOSIO_DISPATCH( addressbook, (upsert))
