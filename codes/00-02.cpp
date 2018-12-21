#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>

using namespace eosio;
using namespace std;

class [[eosio::contract("eosio.token")]] token : public contract {
public:
    using contract::contract;
    
    [[eosio::action]]
    void issue( name to, asset quantity, string memo );
    
private:
    struct [[eosio::table]] account {
        asset balance;
        
        uint64_t primary_key() const { return balance.symbol.code().raw(); }
    }
    
    typedef eosio::multi_index< "accounts"_n, account > accounts;
    
    void add_balance ( name owner, asset value, name ram_payer ) {
        accounts to_acnts( _self, owner.value );
        auto to = to_acnts.find( value.symbol.code().raw() );
        
        if (to == to_acnts.end() ) {
            to_acnts.emplace( ram_payer, [&]( auto& a ){
                a.balance = value;
            });
        } else {
            to_acnts.modify( to, same_payer, [&]( auto& a ){
                a.balance += value;
            });
        }
    }
};

EOSIO_DISPATCH( token, (issue) )
