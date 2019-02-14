#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>

using namespace eosio;

class [[eosio::contract]] hello : public contract {
public:
    using contract::contract;
    
    [[eosio::action]]
    void hi( name user ) {
        print("Hello, ", name{user});
    }
};

EOSIO_DISPATCH( hello, (hi))

