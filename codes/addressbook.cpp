#include <eosiolib/eosio.hpp>

using namespace eosio;
using namespace std;

class [[eosio::contract]] addressbook : public contract {
    private:
        struct [[eosio::table]] person {
            name key;
            string first_name;
            string last_name;
            string phone;

            uint64_t primary_key() const { return key.value; }
        };  

        typedef multi_index<"people"_n, person> adrs;

    public:
        using contract::contract;

        [[eosio::action]]
        void upsert (name key, string first_name, string last_name, string phone) { 
            adrs adrstable(_code, _code.value);
            auto existing = adrstable.find(key.value);

            if (existing == adrstable.end()) {
                adrstable.emplace(key, [&](auto& row){
                    row.key = key;
                    row.first_name = first_name;
                    row.last_name = last_name;
                    row.phone = phone;
                }); 
            } else {
                adrstable.modify(existing, key, [&](auto& row){
                    row.key = key;
                    row.first_name = first_name;
                    row.last_name = last_name;
                    row.phone = phone;
                }); 
            }   
        }   
};

EOSIO_DISPATCH(addressbook, (upsert))