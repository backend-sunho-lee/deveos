/*
 * @author sunny
 * 2019-02-15
 */

#include <eosiolib/eosio.hpp>
#include <eosiolib/asset.hpp>
#include <eosiolib/print.hpp>

using namespace eosio;

class [[eosio::contract("simple.token")]] token : public contract {
private:
    struct [[eosio::table]] account {
        name owner;
        asset balance;
        
        uint64_t primary_key() const { return owner.value; }
    };
    typedef multi_index<"accounts"_n, account> _accounts;
    
    void add_balance(name to, asset quantity){
        _accounts acnt(_self, _self.value);
        
        auto existing = acnt.find(to.value);
        if (existing == acnt.end()) {
            acnt.emplace(_self, [&](auto& row){
                row.owner = to;
                row.balance = quantity;
            });
        } else {
            acnt.modify(existing, _self, [&](auto& row){
                row.balance += quantity;
            });
        }
    }
    
    void sub_balance(name to, asset quantity){
        _accounts acnt(_self, _self.value);
        auto existing = acnt.find(to.value);
        acnt.modify(existing, _self, [&](auto& row){
            row.balance -= quantity;
        });
    }
    
public:
    using contract::contract;
    
    [[eosio::action]] void issue(name to, asset quantity){
        add_balance(to, quantity);
        print(quantity, " issue to ", to);
    }
    
    [[eosio::action]] void transfer(name from, name to, asset quantity){
        sub_balance(from, quantity);
        add_balance(to, quantity);
        print(from, " send ", quantity, " to ", to);
    }
};

EOSIO_DISPATCH(token, (issue)(transfer))
