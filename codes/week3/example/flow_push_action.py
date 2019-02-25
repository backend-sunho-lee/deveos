# https://developers.eos.io/eosio-nodeos/reference#push_transaction
# EOSIO RPC API의 push_transaction API를 요청하려면 signatures, compression, packed_context_free_data, packed_trx 데이터를 보내야 하는데, 그 데이터들을 만드는 것부터 전송까지 이뤄지는 함수다.. 개빡시다
def push_transaction(self, transaction, keys, broadcast=True, compression='none', timeout=30) :
    ''' parameter keys can be a list of WIF strings or EOSKey objects or a filename to key file'''
    
    # 1. get_chain_lib_info: 연결할 체인(노드)의 정보를 받는 API 호출하기
    chain_info,lib_info = self.get_chain_lib_info()
    def get_chain_lib_info(self, timeout=30) :
        # https://developers.eos.io/eosio-nodeos/reference#get_info
        chain_info = self.get('chain.get_info', timeout=timeout)
            # get method 호출
            def get(self, func='', **kwargs) :  # func = 'chain.get_info'
                # DynamicUrl 호출 - dybamic_url.py
                cmd = eval('self._dynurl.{0}'.format(func))
                
                # 입력받은 func = chain.get_info라는 문자로 /v1/chain/get_info URL 생성
                url = cmd.create_url()
                
                # 생성한 URL API를 GET 메소드로 호출
                # 파이썬의 requests 패키지를 사용하여 API를 호출한다
                # 이전까지는 API를 호출하기 위한 작업을 처리한 것. 번거로워보이지만 범용성, 재활용을 위해 이렇게 코드를 만든 것
                # API의 응답을 return 해준다 = chain_info
                return cmd.get_url(url, **kwargs)
                def get_url(self, url, params=None, json=None, timeout=30) :
                    # get request
                    r = requests.get(url,params=params, json=json, timeout=timeout)
                    r.raise_for_status()
                    return r.json()     # chain_info
        
        # chain_info의 last_irreversible_block_num은 특정 블록번호를 지칭한다
        # 블록번호에 해당하는 정보를 획득하여 lib_info에 담는다
        lib_info = self.get_block(chain_info['last_irreversible_block_num'], timeout=timeout)
        def get_block(self, block_num, timeout=30) :
            # post method 호출
            # https://developers.eos.io/eosio-nodeos/reference#get_block
            return self.post('chain.get_block', params=None, json={'block_num_or_id' : block_num}, timeout=timeout)
            def post(self, func='', **kwargs) :
                cmd = eval('self._dynurl.{0}'.format(func))
                url = cmd.create_url()
                return cmd.post_url(url, **kwargs)  # lib_info
                def post_url(self, url, params=None, json=None, data=None, timeout=30) :
                    # post request
                    r = requests.post(url,params=params, json=json, data=data, timeout=timeout)
                    try :
                        r.raise_for_status()
                    except :
                        raise requests.exceptions.HTTPError('Error: {}'.format(r.json()))
                    return r.json()
        return chain_info, lib_info





    # 2. 트랜잭션에 넣을 데이터를 이오스가 원하는 형식으로 맞춰주는 작업 (1)
    # types.py - Transaction 클래스 객체 생성
    trx = Transaction(transaction, chain_info, lib_info)    # transaction은 push_action()의 매개변수로 넘어온 값
    class Transaction(BaseObject) :
        def __init__(self, d, chain_info, lib_info) :
            # add defaults - 만료기한, 참조블럭
            if 'expiration' not in d :
                d['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=30)).replace(tzinfo=pytz.UTC))
            if 'ref_block_num' not in d :
                d['ref_block_num'] = chain_info['last_irreversible_block_num'] & 0xFFFF
            if 'ref_block_prefix' not in d :
                d['ref_block_prefix'] = lib_info['ref_block_prefix']
            
            # validate, 유효성 검사
            # 트랜잭션을 전송할 수 있도록 입력된 데이터의 형식(데이터 타입, 입력 방식) 등을 정해진대로 만드는 작업
            self._validator = TransactionSchema()
            class TransactionSchema(colander.MappingSchema):
                # header
                expiration = TimeSchema()
                ref_block_num = RefBlockNumSchema()
                ref_block_prefix = RefBlockPrefixSchema()
                net_usage_words = NetUsageWordsSchema()
                max_cpu_usage_ms = MaxCpuUsageMsSchema()
                delay_sec = DelaySecSchema()
                # body
                context_free_actions = ContextActionsSchema()
                actions = ActionsSchema()
                transaction_extensions = ExtensionsSchema()
            
            super(Transaction, self).__init__(d)
            
            # parse actions
            self.actions = self._create_obj_array(self.actions, Action)
    
    
    
    
    
    # 3. 트랜잭션에 넣을 데이터를 이오스가 원하는 형식으로 맞춰주는 작업 (2) - 인코딩 방식 변경
    # utils.py
    digest = sig_digest(trx.encode(), chain_info['chain_id'])   # chain_id = 연결할 노드의 아이디
    def sig_digest(payload, chain_id=None, context_free_data=None) :
        if chain_id :
            buf = bytearray.fromhex(chain_id)
        else :
            buf = bytearray(32)
        
        # already a bytearray
        buf.extend(payload)
        if context_free_data :
            #buf += sha256(context_free_data)
            pass
        else :
            # empty buffer
            buf.extend(bytearray(32))
        
        return sha256(buf)

            

            
            
    # 4. API에 맞는 key 형식에 따라 keys 배열 생성
    # utils.py
    # sign the transaction. 트랜잭션을 여러개 보낼 수 있으니 keys로 한 것. 여러개의 키를 받기위해서
    signatures = []
    
    if os.path.isfile(keys):
        keys = parse_key_file(keys, first_key=False)
        # .key 파일로 넘겨진 경우, 파일에서 Private Key 꺼내기
        def parse_key_file(filename, first_key=True):
            keys=[]
            with open(filename) as fo:
                lines = fo.readlines()
                for line in lines:
                    if line.startswith('Private'):
                        try:
                            header,key = line.replace(' ', '').rstrip().split(':')
                            if key and first_key:
                                return key
                            elif key:
                                keys.append(key)
                    except ValueError:
                        # invalid format
                        pass
            if keys:
                return keys
            raise exceptions.InvalidKeyFile('Key file was in an invalid format. Must contain one key pair and have a prefix of "Private key:"')
    elif not isinstance(keys, list) :
        keys = [keys]





    # 5. private key 배열인 keys로 EOSKey 객체로 만드는 작업
    # keys.py
    for key in keys :
        # wallet 포맷 형식에 맞는지 확인
        # wif = Wallet Import Format의 약자
        if check_wif(key) :
        def check_wif(key) :
            if isinstance(key, str) :
                try :
                    EOSKey(key) # key = Private Key
                    return True
                    except Exception as ex:
                        pass
            return False
            
            # private key를 가지고 EOSKey 클래스의 객체를 만든다
            k = EOSKey(key)
            class EOSKey :
                def __init__(self, private_str='') :
                    if private_str :
                        private_key, format, key_type = self._parse_key(private_str)
                        # ecdsa: 타원곡선을 이용한 전자서명 알고리즘
                        self._sk = ecdsa.SigningKey.from_string(unhexlify(private_key), curve=ecdsa.SECP256k1)
                    else :
                        prng = self._create_entropy()
                        self._sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=prng)
                        self._vk = self._sk.get_verifying_key()

                def __str__(self) :
                    return self.to_public()

                def _parse_key(self, private_str) :
                    match = re.search('^PVT_([A-Za-z0-9]+)_([A-Za-z0-9]+)$', private_str)
                    if not match :
                        # legacy WIF - format
                        version_key = self._check_decode(private_str, 'sha256x2')
                        # ensure first 2 chars == 0x80
                        version = int(version_key[0:2],16)
                    
                    if not version == 0x80 :
                        raise ValueError('Expected version 0x80, instead got {0}', version)
                        private_key = version_key[2:]
                        key_type = 'K1'
                        format = 'WIF'
                    else :
                        key_type, key_string = match.groups()
                        private_key = self._check_decode(key_string, key_type)
                        format = 'PVT'
                    return (private_key, format, key_type)

                def _create_entropy(self) :
                    ba = bytearray(os.urandom(32))
                    seed = sha256(ba)
                    return ecdsa.util.PRNG(seed)
            
            elif isinstance(key, EOSKey) :
                k = key
            else :
                raise EOSKeyError('Must pass a WIF string or EOSKey')
            
            
            
            
            
            # 6. 트랜잭션에 계정 싸인 하는 작업 (EOSKey+digest)
            # digest = 트랜잭션에 담을 데이터를 바이너리로 인코딩한 것
            # 여러개의 트랜잭션을 담을 수 있으니까 signatures 배열에 여러개를 담을 수 있도록 만든 거
            signatures.append(k.sign(digest))   # k = EOSKey 객체
            def sign(self, digest) :
                cnt = 0
                
                # convert digest to hex string
                digest = unhexlify(digest)
                
                while 1 :
                    cnt +=1
                    if not cnt % 10 :
                        print('Still searching for a signature. Tried {} times.'.format(cnt))
                    
                    # get deterministic k
                    k = ecdsa.rfc6979.generate_k(
                        self._sk.curve.generator.order(),
                        self._sk.privkey.secret_multiplier,
                        hashlib.sha256,
                        bytearray(sha256(digest + struct.pack('d', time.time())), 'utf-8') # use time to randomize
                    )
                    
                    # sign the message
                    sigder = self._sk.sign_digest(digest, sigencode=ecdsa.util.sigencode_der, k=k)

                    # reformat sig
                    r, s = ecdsa.util.sigdecode_der(sigder, self._sk.curve.generator.order())
                    sig = ecdsa.util.sigencode_string(r, s, self._sk.curve.generator.order())

                    # ensure signature is canonical
                    # 이제 진짜 정식으로 signature를 만드는 작업
                    if isinstance(sigder[5],int) :
                        lenR = sigder[3]
                    else :
                        lenR =  str_to_hex(sigder[3])
                    
                    if isinstance(sigder[5 + lenR], int) :
                        lenS = sigder[5 + lenR]
                    else :
                        lenS = str_to_hex(sigder[5 + lenR])
                    
                    if lenR is 32 and lenS is 32 :
                        # derive recover parameter
                        i = self._recovery_pubkey_param(digest, sig)
                        # compressed
                        i += 4
                        # compact
                        i += 27
                        break
                        
                # pack
                sigstr = struct.pack('<B', i) + sig
                # encode
                return 'SIG_K1_' + self._check_encode(hexlify(sigstr), 'K1').decode()





    # 7. API 요청시 보낼 데이터에 담아준다
    final_trx = {
        'compression' : compression,
        'transaction' : trx.__dict__,
        'signatures' : signatures
    }

    # API 요청 데이터를 JSON 타입으로 보내야해서 JSON으로 바꿔준다
    data = json.dumps(final_trx, cls=EOSEncoder)

    if broadcast :  # push_action의 broadcast 변수 = True
        return self.post('chain.push_transaction', params=None, data=data, timeout=timeout)
    return data
