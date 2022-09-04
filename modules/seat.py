import hashlib

class SeatInfo:
    def __init__(self) -> None:
        self.hash = 0
        self.classroom = ""
        self.seat_no = 0

class SeatHelper:
    hasher = hashlib.md5()
    # "hash": ("room", number)
    seat_hash_dict = {
        "8096392c15c36738c139edd067241289": ("R302", 1),
        "838bd05838f3c403c81dbe8a989850dc": ("R302", 2),
        "f2d0f8c137c057e48a9497df883f613a": ("R302", 3),
        "8359e82e00609b5e6aa16637c7c893ed": ("R302", 4),
        "b0cc1e48318ce88e790b3b22dde57631": ("R302", 5),
        "4bafbafe329bc27197e20ace0756736d": ("R302", 6),
        "ba16248e38e16691a3e6a7b41ed68ff8": ("R302", 7),
        "f40e14e25382a2b31dfa0acaf30118ee": ("R302", 8),
        "a60008eee145b6db9a9353de44e2083e": ("R302", 9),
        "49efa5fb6bf6981da0dc62136c870889": ("R302", 10),
        "009d1306629655cdeadcd771523ecdb0": ("R302", 11),
        "b3748fdc7320248b114375dd8aecba41": ("R302", 12),
        "79f448d09a08d1613eddfd678804f44e": ("R302", 13),
        "2cfb0567f528527a4401f9da603847af": ("R302", 14),
        "88ef40e41e48cd44aa494fd9f4f70532": ("R302", 15),
        "69209141c7b1c7d318c6d9de7512bd48": ("R302", 16),
        "4366feb05034a8a496faf6f27f996cb4": ("R302", 17),
        "7a512fd4bc7d5b6a44caeb21ecaf692b": ("R302", 18),
        "3b604d70f57cb419615396659c6d11c5": ("R302", 19),
        "b99e4dbbbf9c05d82dbcd23469350c95": ("R302", 20),
        "c504ffb87044ae8a18c0f663c22f184c": ("R302", 21),
        "cb96e1969f0199723ae8ba672fd2e14b": ("R302", 22),
        "5ad8b5312de10861eefb57250b289b29": ("R302", 23),
        "d77d55b66d717cad45491b77631ac0a6": ("R302", 24),
        "d94da9bdae3dc00993a0c0ff257f09eb": ("R302", 25),
        "2dd3c03f411fc420591a336ff1039841": ("R302", 26),
        "8b12f3f1e2b5544fa48541b65008f9c9": ("R302", 27),
        "e1bd4577ab249e530d66e8a1df9c0d61": ("R302", 28),
        "a1cd153479469f5bdeb78cd5b70dd832": ("R302", 29),
        "868cb65ce8287ea3ab5f12ba2691a0ff": ("R302", 30),
        "cabf52dfc24df55381ef5a4718bff9ec": ("R302", 31),
        "23ac38389c6c1d9701658f2bbf343708": ("R401", 1),
        "94445d4dd3e212cba1d3c8824e7c3ee1": ("R401", 2),
        "fae97c9a5a9e0713ae5d75dca9c38a54": ("R401", 3),
        "cc7e16417b72b006559e57f4ad3e8b80": ("R401", 4),
        "363df049db771689e0881061ba71a2da": ("R401", 5),
        "520713f50cc983d137830cad8589309a": ("R401", 6),
        "25c2742b1c939365b9900225b3b78e2a": ("R401", 7),
        "850997d57707183985d3de3dff268ef3": ("R401", 8),
        "7f6fd854ed7bd68f6db7427427ed12d8": ("R401", 9),
        "851ff68c6135d3f2e202d319c0c4ae95": ("R401", 10),
        "1f03a84b35f574c236abdd91ad10b25c": ("R401", 11),
        "43e8572304ef9a5470f768c4e2529d3c": ("R401", 12),
        "2f442cb4c1431e24ea32763a18f1970a": ("R401", 13),
        "15d6a7e504e81298ffe73800992e685c": ("R401", 14),
        "d36f5aa5e6afca2dd25ab5c67c6aa760": ("R401", 15),
        "7468a9c719289100e7bc1c05a0665c22": ("R401", 16),
        "f786d57e46838254726f0150875ded71": ("R401", 17),
        "6ddf6f7c937ef09b336be04f03415c88": ("R401", 18),
        "f54de1416e66df2ebe788a3151a5b3a0": ("R401", 19),
        "67a7b9fb2c8d2bf9b15d817b61ad4e21": ("R401", 20),
        "23881a22ba139071c8e873fc01dbe25f": ("R401", 21),
        "d1ce0128124ccdc38fede0ea50fab274": ("R401", 22),
        "b632725775bcf67a81a1f9bcf36356d1": ("R401", 23),
        "98bc5b462ab86b450f935cba932cbe76": ("R401", 24),
        "9e729574ae5688d202250392ab002c81": ("R401", 25),
        "092ac3bc27895d58ff78bacaaaa4aaa6": ("R401", 26),
        "0fcf32c6a1a8744e36d197230c18be17": ("R401", 27),
        "951b2d6ba2aee0cc2f89aa96aa7ce4b1": ("R401", 28),
        "f7079efe2801ea4418912d490e3ac07e": ("R401", 29),
        "9bb735a45b180c9490767a5b831d557e": ("R401", 30),
        "7d4a8a7e66312424cd139e2f7179bb29": ("R401", 31),
        "d2964a8178605ed4d0fb288d29aa22c5": ("電腦B", 1),
        "6babd1d1494e62e8db142a15d03bb9e0": ("電腦B", 2),
        "7f736acd5ee9e48f187c8f2e2e425b8b": ("電腦B", 3),
        "755d09ac31dfb133f6cfc73cef885939": ("電腦B", 4),
        "5b864715296c105c1402ec73ba5751f5": ("電腦B", 5),
        "0b1aa33101b5164b17faf55f063de593": ("電腦B", 6),
        "23e746f2612dd5888493513ef8a7a920": ("電腦B", 7),
        "3135d95db8923e6365013b67a8a5bf67": ("電腦B", 8),
        "28099fb2a685a4e88d86d130d8b4ad6e": ("電腦B", 9),
        "ed71a141033dc30b640b2fb33f8c1b1d": ("電腦B", 10),
        "c6a906a9c424ecdea4f6778e792b9bd7": ("電腦B", 11),
        "2eca95657976f33c370690ae09d31b15": ("電腦B", 12),
        "0266db336d6e28ad14d24a34a057d3e6": ("電腦B", 13),
        "562f603c19423fc298f5a1a5cda6e951": ("電腦B", 14),
        "0894bf72dc176c0e9d957e522719d732": ("電腦B", 15),
        "f5fbd105b6eb50d5b4b052c86c7493d4": ("電腦B", 16),
        "43d7b4c51b58faa325e12a0e26d08f21": ("電腦B", 17),
        "4db3e15848ebfac4c40593ef9419392b": ("電腦B", 18),
        "2a2bdff3ece153282437d76a599a86ea": ("電腦B", 19),
        "522cbcaa27307c5d8d05b646886ce807": ("電腦B", 20),
        "823d1d73eff645ab5526d43eda06741b": ("電腦B", 21),
        "396e3121b11d0477c05e92adff5ad10c": ("電腦B", 22),
        "006f1086954b2f4f3332bcbe29564fd4": ("電腦B", 23),
        "59b255c96874a10b7bdea705ea24cf69": ("電腦B", 24),
        "c94b11e8b0b34c6a0639024e58725826": ("電腦B", 25),
        "f5a2d40d8ab903bb8fcf188130d6b18f": ("電腦B", 26),
        "f554d85eac160bec6aa6c73c83b71152": ("電腦B", 27),
        "4dd11f5c61152361e962ac4ddd121fdc": ("電腦B", 28),
        "b361eed688a04d1327342e3cfd09915e": ("電腦B", 29),
        "70ad591c404c61d17905d47efc0a52f7": ("電腦B", 30),
        "6b7827eb3427ba6f15ac645dfb333a2a": ("電腦B", 31),
        "ab10b43e177442a6c9ce480a3a00fd9e": ("TEAL", 1),
        "10c7d943d0803e1e61e49b9009e91f63": ("TEAL", 2),
        "539bf521151e6db6b099fe79d13b465c": ("TEAL", 3),
        "fd46970b92c73d31ec3d99e2662016a3": ("TEAL", 4),
        "3af446118f2e1e6a62ef5e84cece9122": ("TEAL", 5),
        "d3fab0528bcf361faaf333ae299a2aa1": ("TEAL", 6),
        "32c22a5aa0d9db057bb32a7a0dea4538": ("TEAL", 7),
        "45dc015458e4f9500dded554f9a7711f": ("TEAL", 8),
        "2eabbf76aeb6770603963b0a33e84410": ("TEAL", 9),
        "dc49b83e87eb9fe715b7c40d9cda0840": ("TEAL", 10),
        "df1cbc81de6d67bd63c6b8ee19d2fa6d": ("TEAL", 11),
        "11209814500f2be629abe4f4710daa86": ("TEAL", 12),
        "0f088d1e12f067c3f5ef7fc1fb3c621f": ("TEAL", 13),
        "ce6d76a63ecd9bf3448b55bda747cc45": ("TEAL", 14),
        "c873c26b922d9f23de578cb6c9c1099b": ("TEAL", 15),
        "f551fa3234a211cce408c86b3eca9d34": ("TEAL", 16),
        "9650ffce457b840bd92bc44c418780f3": ("TEAL", 17),
        "324688680453d4301e48eb900bb3ba25": ("TEAL", 18),
        "400aba669a2d3a52425d2103e81e58f4": ("TEAL", 19),
        "1f18d0c2793f219743b6c8008c4d6c11": ("TEAL", 20),
        "c666e2c814a67607fca218daae2ceb82": ("TEAL", 21),
        "edfbbcf3966230fb08046403e4399d2e": ("TEAL", 22),
        "1f51524d343d4a03b8b48b0391054896": ("TEAL", 23),
        "222fc5bab79177effde1ca4a49cbc592": ("TEAL", 24),
        "115400232aa9bc112033520f48c3a01b": ("TEAL", 25),
        "cbb98b7cef1727ad485d3c01b4822267": ("TEAL", 26),
        "4c00a66db06e9b420d123a3d2cd0b0be": ("TEAL", 27),
        "a6b630776c6833272dca438b37c8ae32": ("TEAL", 28),
        "4ba4cacf07d862cde4e287046f7f8675": ("TEAL", 29),
        "66b670e16e6e1496f18dfc285b930ace": ("TEAL", 30),
        "e25601a144e9d64b7241f9db9f9cd8d1": ("TEAL", 31)
    }

    def __init__(self) -> None:
        pass

    def get_seat_info(self, form_data: dict) -> SeatInfo:
        seat_hash = form_data["seat_hash"]
        seat_item = SeatHelper.seat_hash_dict.get(seat_hash)
        seat_info = SeatInfo()
        seat_info.hash = seat_hash
        seat_info.classroom = seat_item[0]
        seat_info.seat_no = seat_item[1]
        return seat_info

    def get_seat_hash(self, classroom: str, seat_no: int) -> str:
        SeatHelper.hasher.update(
            f"{classroom}-{str(seat_no).zfill(2)}"
        )
        hash_bytes = SeatHelper.hasher.digest()
        return hash_bytes.decode('utf-8')
