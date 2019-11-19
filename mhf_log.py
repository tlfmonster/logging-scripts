# Monster Hunter Frontier Packet logger made by Ando.
#
# Requires Frida, install with:
#   `py -3 -m pip install frida`
# 
# Run in an administrator command prompt with:
#   `py -3 mhf_jp_log.py mhf.exe`

import frida
import sys
import struct
import binascii
from datetime import datetime
from enum import Enum

class PacketType(Enum):
    MSG_HEAD = 0
    MSG_SYS_reserve01 = 1
    MSG_SYS_reserve02 = 2
    MSG_SYS_reserve03 = 3
    MSG_SYS_reserve04 = 4
    MSG_SYS_reserve05 = 5
    MSG_SYS_reserve06 = 6
    MSG_SYS_reserve07 = 7
    MSG_SYS_ADD_OBJECT = 8
    MSG_SYS_DEL_OBJECT = 9
    MSG_SYS_DISP_OBJECT = 10
    MSG_SYS_HIDE_OBJECT = 11
    MSG_SYS_reserve0C = 12
    MSG_SYS_reserve0D = 13
    MSG_SYS_reserve0E = 14
    MSG_SYS_EXTEND_THRESHOLD = 15
    MSG_SYS_END = 16
    MSG_SYS_NOP = 17
    MSG_SYS_ACK = 18
    MSG_SYS_TERMINAL_LOG = 19
    MSG_SYS_LOGIN = 20
    MSG_SYS_LOGOUT = 21
    MSG_SYS_SET_STATUS = 22
    MSG_SYS_PING = 23
    MSG_SYS_CAST_BINARY = 24
    MSG_SYS_HIDE_CLIENT = 25
    MSG_SYS_TIME = 26
    MSG_SYS_CASTED_BINARY = 27
    MSG_SYS_GET_FILE = 28
    MSG_SYS_ISSUE_LOGKEY = 29
    MSG_SYS_RECORD_LOG = 30
    MSG_SYS_ECHO = 31
    MSG_SYS_CREATE_STAGE = 32
    MSG_SYS_STAGE_DESTRUCT = 33
    MSG_SYS_ENTER_STAGE = 34
    MSG_SYS_BACK_STAGE = 35
    MSG_SYS_MOVE_STAGE = 36
    MSG_SYS_LEAVE_STAGE = 37
    MSG_SYS_LOCK_STAGE = 38
    MSG_SYS_UNLOCK_STAGE = 39
    MSG_SYS_RESERVE_STAGE = 40
    MSG_SYS_UNRESERVE_STAGE = 41
    MSG_SYS_SET_STAGE_PASS = 42
    MSG_SYS_WAIT_STAGE_BINARY = 43
    MSG_SYS_SET_STAGE_BINARY = 44
    MSG_SYS_GET_STAGE_BINARY = 45
    MSG_SYS_ENUMERATE_CLIENT = 46
    MSG_SYS_ENUMERATE_STAGE = 47
    MSG_SYS_CREATE_MUTEX = 48
    MSG_SYS_CREATE_OPEN_MUTEX = 49
    MSG_SYS_DELETE_MUTEX = 50
    MSG_SYS_OPEN_MUTEX = 51
    MSG_SYS_CLOSE_MUTEX = 52
    MSG_SYS_CREATE_SEMAPHORE = 53
    MSG_SYS_CREATE_ACQUIRE_SEMAPHORE = 54
    MSG_SYS_DELETE_SEMAPHORE = 55
    MSG_SYS_ACQUIRE_SEMAPHORE = 56
    MSG_SYS_RELEASE_SEMAPHORE = 57
    MSG_SYS_LOCK_GLOBAL_SEMA = 58
    MSG_SYS_UNLOCK_GLOBAL_SEMA = 59
    MSG_SYS_CHECK_SEMAPHORE = 60
    MSG_SYS_OPERATE_REGISTER = 61
    MSG_SYS_LOAD_REGISTER = 62
    MSG_SYS_NOTIFY_REGISTER = 63
    MSG_SYS_CREATE_OBJECT = 64
    MSG_SYS_DELETE_OBJECT = 65
    MSG_SYS_POSITION_OBJECT = 66
    MSG_SYS_ROTATE_OBJECT = 67
    MSG_SYS_DUPLICATE_OBJECT = 68
    MSG_SYS_SET_OBJECT_BINARY = 69
    MSG_SYS_GET_OBJECT_BINARY = 70
    MSG_SYS_GET_OBJECT_OWNER = 71
    MSG_SYS_UPDATE_OBJECT_BINARY = 72
    MSG_SYS_CLEANUP_OBJECT = 73
    MSG_SYS_reserve4A = 74
    MSG_SYS_reserve4B = 75
    MSG_SYS_reserve4C = 76
    MSG_SYS_reserve4D = 77
    MSG_SYS_reserve4E = 78
    MSG_SYS_reserve4F = 79
    MSG_SYS_INSERT_USER = 80
    MSG_SYS_DELETE_USER = 81
    MSG_SYS_SET_USER_BINARY = 82
    MSG_SYS_GET_USER_BINARY = 83
    MSG_SYS_NOTIFY_USER_BINARY = 84
    MSG_SYS_reserve55 = 85
    MSG_SYS_reserve56 = 86
    MSG_SYS_reserve57 = 87
    MSG_SYS_UPDATE_RIGHT = 88
    MSG_SYS_AUTH_QUERY = 89
    MSG_SYS_AUTH_DATA = 90
    MSG_SYS_AUTH_TERMINAL = 91
    MSG_SYS_reserve5C = 92
    MSG_SYS_RIGHTS_RELOAD = 93
    MSG_SYS_reserve5E = 94
    MSG_SYS_reserve5F = 95
    MSG_MHF_SAVEDATA = 96
    MSG_MHF_LOADDATA = 97
    MSG_MHF_LIST_MEMBER = 98
    MSG_MHF_OPR_MEMBER = 99
    MSG_MHF_ENUMERATE_DIST_ITEM = 100
    MSG_MHF_APPLY_DIST_ITEM = 101
    MSG_MHF_ACQUIRE_DIST_ITEM = 102
    MSG_MHF_GET_DIST_DESCRIPTION = 103
    MSG_MHF_SEND_MAIL = 104
    MSG_MHF_READ_MAIL = 105
    MSG_MHF_LIST_MAIL = 106
    MSG_MHF_OPRT_MAIL = 107
    MSG_MHF_LOAD_FAVORITE_QUEST = 108
    MSG_MHF_SAVE_FAVORITE_QUEST = 109
    MSG_MHF_REGISTER_EVENT = 110
    MSG_MHF_RELEASE_EVENT = 111
    MSG_MHF_TRANSIT_MESSAGE = 112
    MSG_SYS_reserve71 = 113
    MSG_SYS_reserve72 = 114
    MSG_SYS_reserve73 = 115
    MSG_SYS_reserve74 = 116
    MSG_SYS_reserve75 = 117
    MSG_SYS_reserve76 = 118
    MSG_SYS_reserve77 = 119
    MSG_SYS_reserve78 = 120
    MSG_SYS_reserve79 = 121
    MSG_SYS_reserve7A = 122
    MSG_SYS_reserve7B = 123
    MSG_SYS_reserve7C = 124
    MSG_CA_EXCHANGE_ITEM = 125
    MSG_SYS_reserve7E = 126
    MSG_MHF_PRESENT_BOX = 127
    MSG_MHF_SERVER_COMMAND = 128
    MSG_MHF_SHUT_CLIENT = 129
    MSG_MHF_ANNOUNCE = 130
    MSG_MHF_SET_LOGINWINDOW = 131
    MSG_SYS_TRANS_BINARY = 132
    MSG_SYS_COLLECT_BINARY = 133
    MSG_SYS_GET_STATE = 134
    MSG_SYS_SERIALIZE = 135
    MSG_SYS_ENUMLOBBY = 136
    MSG_SYS_ENUMUSER = 137
    MSG_SYS_INFOKYSERVER = 138
    MSG_MHF_GET_CA_UNIQUE_ID = 139
    MSG_MHF_SET_CA_ACHIEVEMENT = 140
    MSG_MHF_CARAVAN_MY_SCORE = 141
    MSG_MHF_CARAVAN_RANKING = 142
    MSG_MHF_CARAVAN_MY_RANK = 143
    MSG_MHF_CREATE_GUILD = 144
    MSG_MHF_OPERATE_GUILD = 145
    MSG_MHF_OPERATE_GUILD_MEMBER = 146
    MSG_MHF_INFO_GUILD = 147
    MSG_MHF_ENUMERATE_GUILD = 148
    MSG_MHF_UPDATE_GUILD = 149
    MSG_MHF_ARRANGE_GUILD_MEMBER = 150
    MSG_MHF_ENUMERATE_GUILD_MEMBER = 151
    MSG_MHF_ENUMERATE_CAMPAIGN = 152
    MSG_MHF_STATE_CAMPAIGN = 153
    MSG_MHF_APPLY_CAMPAIGN = 154
    MSG_MHF_ENUMERATE_ITEM = 155
    MSG_MHF_ACQUIRE_ITEM = 156
    MSG_MHF_TRANSFER_ITEM = 157
    MSG_MHF_MERCENARY_HUNTDATA = 158
    MSG_MHF_ENTRY_ROOKIE_GUILD = 159
    MSG_MHF_ENUMERATE_QUEST = 160
    MSG_MHF_ENUMERATE_EVENT = 161
    MSG_MHF_ENUMERATE_PRICE = 162
    MSG_MHF_ENUMERATE_RANKING = 163
    MSG_MHF_ENUMERATE_ORDER = 164
    MSG_MHF_ENUMERATE_SHOP = 165
    MSG_MHF_GET_EXTRA_INFO = 166
    MSG_MHF_UPDATE_INTERIOR = 167
    MSG_MHF_ENUMERATE_HOUSE = 168
    MSG_MHF_UPDATE_HOUSE = 169
    MSG_MHF_LOAD_HOUSE = 170
    MSG_MHF_OPERATE_WAREHOUSE = 171
    MSG_MHF_ENUMERATE_WAREHOUSE = 172
    MSG_MHF_UPDATE_WAREHOUSE = 173
    MSG_MHF_ACQUIRE_TITLE = 174
    MSG_MHF_ENUMERATE_TITLE = 175
    MSG_MHF_ENUMERATE_GUILD_ITEM = 176
    MSG_MHF_UPDATE_GUILD_ITEM = 177
    MSG_MHF_ENUMERATE_UNION_ITEM = 178
    MSG_MHF_UPDATE_UNION_ITEM = 179
    MSG_MHF_CREATE_JOINT = 180
    MSG_MHF_OPERATE_JOINT = 181
    MSG_MHF_INFO_JOINT = 182
    MSG_MHF_UPDATE_GUILD_ICON = 183
    MSG_MHF_INFO_FESTA = 184
    MSG_MHF_ENTRY_FESTA = 185
    MSG_MHF_CHARGE_FESTA = 186
    MSG_MHF_ACQUIRE_FESTA = 187
    MSG_MHF_STATE_FESTA_U = 188
    MSG_MHF_STATE_FESTA_G = 189
    MSG_MHF_ENUMERATE_FESTA_MEMBER = 190
    MSG_MHF_VOTE_FESTA = 191
    MSG_MHF_ACQUIRE_CAFE_ITEM = 192
    MSG_MHF_UPDATE_CAFEPOINT = 193
    MSG_MHF_CHECK_DAILY_CAFEPOINT = 194
    MSG_MHF_GET_COG_INFO = 195
    MSG_MHF_CHECK_MONTHLY_ITEM = 196
    MSG_MHF_ACQUIRE_MONTHLY_ITEM = 197
    MSG_MHF_CHECK_WEEKLY_STAMP = 198
    MSG_MHF_EXCHANGE_WEEKLY_STAMP = 199
    MSG_MHF_CREATE_MERCENARY = 200
    MSG_MHF_SAVE_MERCENARY = 201
    MSG_MHF_READ_MERCENARY_W = 202
    MSG_MHF_READ_MERCENARY_M = 203
    MSG_MHF_CONTRACT_MERCENARY = 204
    MSG_MHF_ENUMERATE_MERCENARY_LOG = 205
    MSG_MHF_ENUMERATE_GUACOT = 206
    MSG_MHF_UPDATE_GUACOT = 207
    MSG_MHF_INFO_TOURNAMENT = 208
    MSG_MHF_ENTRY_TOURNAMENT = 209
    MSG_MHF_ENTER_TOURNAMENT_QUEST = 210
    MSG_MHF_ACQUIRE_TOURNAMENT = 211
    MSG_MHF_GET_ACHIEVEMENT = 212
    MSG_MHF_RESET_ACHIEVEMENT = 213
    MSG_MHF_ADD_ACHIEVEMENT = 214
    MSG_MHF_PAYMENT_ACHIEVEMENT = 215
    MSG_MHF_DISPLAYED_ACHIEVEMENT = 216
    MSG_MHF_INFO_SCENARIO_COUNTER = 217
    MSG_MHF_SAVE_SCENARIO_DATA = 218
    MSG_MHF_LOAD_SCENARIO_DATA = 219
    MSG_MHF_GET_BBS_SNS_STATUS = 220
    MSG_MHF_APPLY_BBS_ARTICLE = 221
    MSG_MHF_GET_ETC_POINTS = 222
    MSG_MHF_UPDATE_ETC_POINT = 223
    MSG_MHF_GET_MYHOUSE_INFO = 224
    MSG_MHF_UPDATE_MYHOUSE_INFO = 225
    MSG_MHF_GET_WEEKLY_SCHEDULE = 226
    MSG_MHF_ENUMERATE_INV_GUILD = 227
    MSG_MHF_OPERATION_INV_GUILD = 228
    MSG_MHF_STAMPCARD_STAMP = 229
    MSG_MHF_STAMPCARD_PRIZE = 230
    MSG_MHF_UNRESERVE_SRG = 231
    MSG_MHF_LOAD_PLATE_DATA = 232
    MSG_MHF_SAVE_PLATE_DATA = 233
    MSG_MHF_LOAD_PLATE_BOX = 234
    MSG_MHF_SAVE_PLATE_BOX = 235
    MSG_MHF_READ_GUILDCARD = 236
    MSG_MHF_UPDATE_GUILDCARD = 237
    MSG_MHF_READ_BEAT_LEVEL = 238
    MSG_MHF_UPDATE_BEAT_LEVEL = 239
    MSG_MHF_READ_BEAT_LEVEL_ALL_RANKING = 240
    MSG_MHF_READ_BEAT_LEVEL_MY_RANKING = 241
    MSG_MHF_READ_LAST_WEEK_BEAT_RANKING = 242
    MSG_MHF_ACCEPT_READ_REWARD = 243
    MSG_MHF_GET_ADDITIONAL_BEAT_REWARD = 244
    MSG_MHF_GET_FIXED_SEIBATU_RANKING_TABLE = 245
    MSG_MHF_GET_BBS_USER_STATUS = 246
    MSG_MHF_KICK_EXPORT_FORCE = 247
    MSG_MHF_GET_BREAK_SEIBATU_LEVEL_REWARD = 248
    MSG_MHF_GET_WEEKLY_SEIBATU_RANKING_REWARD = 249
    MSG_MHF_GET_EARTH_STATUS = 250
    MSG_MHF_LOAD_PARTNER = 251
    MSG_MHF_SAVE_PARTNER = 252
    MSG_MHF_GET_GUILD_MISSION_LIST = 253
    MSG_MHF_GET_GUILD_MISSION_RECORD = 254
    MSG_MHF_ADD_GUILD_MISSION_COUNT = 255
    MSG_MHF_SET_GUILD_MISSION_TARGET = 256
    MSG_MHF_CANCEL_GUILD_MISSION_TARGET = 257
    MSG_MHF_LOAD_OTOMO_AIROU = 258
    MSG_MHF_SAVE_OTOMO_AIROU = 259
    MSG_MHF_ENUMERATE_GUILD_TRESURE = 260
    MSG_MHF_ENUMERATE_AIROULIST = 261
    MSG_MHF_REGIST_GUILD_TRESURE = 262
    MSG_MHF_ACQUIRE_GUILD_TRESURE = 263
    MSG_MHF_OPERATE_GUILD_TRESURE_REPORT = 264
    MSG_MHF_GET_GUILD_TRESURE_SOUVENIR = 265
    MSG_MHF_ACQUIRE_GUILD_TRESURE_SOUVENIR = 266
    MSG_MHF_ENUMERATE_FESTA_INTERMEDIATE_PRIZE = 267
    MSG_MHF_ACQUIRE_FESTA_INTERMEDIATE_PRIZE = 268
    MSG_MHF_LOAD_DECO_MYSET = 269
    MSG_MHF_SAVE_DECO_MYSET = 270
    MSG_MHF_reserve010F = 271
    MSG_MHF_LOAD_GUILD_COOKING = 272
    MSG_MHF_REGIST_GUILD_COOKING = 273
    MSG_MHF_LOAD_GUILD_ADVENTURE = 274
    MSG_MHF_REGIST_GUILD_ADVENTURE = 275
    MSG_MHF_ACQUIRE_GUILD_ADVENTURE = 276
    MSG_MHF_CHARGE_GUILD_ADVENTURE = 277
    MSG_MHF_LOAD_LEGEND_DISPATCH = 278
    MSG_MHF_LOAD_HUNTER_NAVI = 279
    MSG_MHF_SAVE_HUNTER_NAVI = 280
    MSG_MHF_REGIST_SPABI_TIME = 281
    MSG_MHF_GET_GUILD_WEEKLY_BONUS_MASTER = 282
    MSG_MHF_GET_GUILD_WEEKLY_BONUS_ACTIVE_COUNT = 283
    MSG_MHF_ADD_GUILD_WEEKLY_BONUS_EXCEPTIONAL_USER = 284
    MSG_MHF_GET_TOWER_INFO = 285
    MSG_MHF_POST_TOWER_INFO = 286
    MSG_MHF_GET_GEM_INFO = 287
    MSG_MHF_POST_GEM_INFO = 288
    MSG_MHF_GET_EARTH_VALUE = 289
    MSG_MHF_DEBUG_POST_VALUE = 290
    MSG_MHF_GET_PAPER_DATA = 291
    MSG_MHF_GET_NOTICE = 292
    MSG_MHF_POST_NOTICE = 293
    MSG_MHF_GET_BOOST_TIME = 294
    MSG_MHF_POST_BOOST_TIME = 295
    MSG_MHF_GET_BOOST_TIME_LIMIT = 296
    MSG_MHF_POST_BOOST_TIME_LIMIT = 297
    MSG_MHF_ENUMERATE_FESTA_PERSONAL_PRIZE = 298
    MSG_MHF_ACQUIRE_FESTA_PERSONAL_PRIZE = 299
    MSG_MHF_GET_RAND_FROM_TABLE = 300
    MSG_MHF_GET_CAFE_DURATION = 301
    MSG_MHF_GET_CAFE_DURATION_BONUS_INFO = 302
    MSG_MHF_RECEIVE_CAFE_DURATION_BONUS = 303
    MSG_MHF_POST_CAFE_DURATION_BONUS_RECEIVED = 304
    MSG_MHF_GET_GACHA_POINT = 305
    MSG_MHF_USE_GACHA_POINT = 306
    MSG_MHF_EXCHANGE_FPOINT_2_ITEM = 307
    MSG_MHF_EXCHANGE_ITEM_2_FPOINT = 308
    MSG_MHF_GET_FPOINT_EXCHANGE_LIST = 309
    MSG_MHF_PLAY_STEPUP_GACHA = 310
    MSG_MHF_RECEIVE_GACHA_ITEM = 311
    MSG_MHF_GET_STEPUP_STATUS = 312
    MSG_MHF_PLAY_FREE_GACHA = 313
    MSG_MHF_GET_TINY_BIN = 314
    MSG_MHF_POST_TINY_BIN = 315
    MSG_MHF_GET_SENYU_DAILY_COUNT = 316
    MSG_MHF_GET_GUILD_TARGET_MEMBER_NUM = 317
    MSG_MHF_GET_BOOST_RIGHT = 318
    MSG_MHF_START_BOOST_TIME = 319
    MSG_MHF_POST_BOOST_TIME_QUEST_RETURN = 320
    MSG_MHF_GET_BOX_GACHA_INFO = 321
    MSG_MHF_PLAY_BOX_GACHA = 322
    MSG_MHF_RESET_BOX_GACHA_INFO = 323
    MSG_MHF_GET_SEIBATTLE = 324
    MSG_MHF_POST_SEIBATTLE = 325
    MSG_MHF_GET_RYOUDAMA = 326
    MSG_MHF_POST_RYOUDAMA = 327
    MSG_MHF_GET_TENROUIRAI = 328
    MSG_MHF_POST_TENROUIRAI = 329
    MSG_MHF_POST_GUILD_SCOUT = 330
    MSG_MHF_CANCEL_GUILD_SCOUT = 331
    MSG_MHF_ANSWER_GUILD_SCOUT = 332
    MSG_MHF_GET_GUILD_SCOUT_LIST = 333
    MSG_MHF_GET_GUILD_MANAGE_RIGHT = 334
    MSG_MHF_SET_GUILD_MANAGE_RIGHT = 335
    MSG_MHF_PLAY_NORMAL_GACHA = 336
    MSG_MHF_GET_DAILY_MISSION_MASTER = 337
    MSG_MHF_GET_DAILY_MISSION_PERSONAL = 338
    MSG_MHF_SET_DAILY_MISSION_PERSONAL = 339
    MSG_MHF_GET_GACHA_PLAY_HISTORY = 340
    MSG_MHF_GET_REJECT_GUILD_SCOUT = 341
    MSG_MHF_SET_REJECT_GUILD_SCOUT = 342
    MSG_MHF_GET_CA_ACHIEVEMENT_HIST = 343
    MSG_MHF_SET_CA_ACHIEVEMENT_HIST = 344
    MSG_MHF_GET_KEEP_LOGIN_BOOST_STATUS = 345
    MSG_MHF_USE_KEEP_LOGIN_BOOST = 346
    MSG_MHF_GET_UD_SCHEDULE = 347
    MSG_MHF_GET_UD_INFO = 348
    MSG_MHF_GET_KIJU_INFO = 349
    MSG_MHF_SET_KIJU = 350
    MSG_MHF_ADD_UD_POINT = 351
    MSG_MHF_GET_UD_MY_POINT = 352
    MSG_MHF_GET_UD_TOTAL_POINT_INFO = 353
    MSG_MHF_GET_UD_BONUS_QUEST_INFO = 354
    MSG_MHF_GET_UD_SELECTED_COLOR_INFO = 355
    MSG_MHF_GET_UD_MONSTER_POINT = 356
    MSG_MHF_GET_UD_DAILY_PRESENT_LIST = 357
    MSG_MHF_GET_UD_NORMA_PRESENT_LIST = 358
    MSG_MHF_GET_UD_RANKING_REWARD_LIST = 359
    MSG_MHF_ACQUIRE_UD_ITEM = 360
    MSG_MHF_GET_REWARD_SONG = 361
    MSG_MHF_USE_REWARD_SONG = 362
    MSG_MHF_ADD_REWARD_SONG_COUNT = 363
    MSG_MHF_GET_UD_RANKING = 364
    MSG_MHF_GET_UD_MY_RANKING = 365
    MSG_MHF_ACQUIRE_MONTHLY_REWARD = 366
    MSG_MHF_GET_UD_GUILD_MAP_INFO = 367
    MSG_MHF_GENERATE_UD_GUILD_MAP = 368
    MSG_MHF_GET_UD_TACTICS_POINT = 369
    MSG_MHF_ADD_UD_TACTICS_POINT = 370
    MSG_MHF_GET_UD_TACTICS_RANKING = 371
    MSG_MHF_GET_UD_TACTICS_REWARD_LIST = 372
    MSG_MHF_GET_UD_TACTICS_LOG = 373
    MSG_MHF_GET_EQUIP_SKIN_HIST = 374
    MSG_MHF_UPDATE_EQUIP_SKIN_HIST = 375
    MSG_MHF_GET_UD_TACTICS_FOLLOWER = 376
    MSG_MHF_SET_UD_TACTICS_FOLLOWER = 377
    MSG_MHF_GET_UD_SHOP_COIN = 378
    MSG_MHF_USE_UD_SHOP_COIN = 379
    MSG_MHF_GET_ENHANCED_MINIDATA = 380
    MSG_MHF_SET_ENHANCED_MINIDATA = 381
    MSG_MHF_SEX_CHANGER = 382
    MSG_MHF_GET_LOBBY_CROWD = 383
    MSG_SYS_reserve180 = 384
    MSG_MHF_GUILD_HUNTDATA = 385
    MSG_MHF_ADD_KOURYOU_POINT = 386
    MSG_MHF_GET_KOURYOU_POINT = 387
    MSG_MHF_EXCHANGE_KOURYOU_POINT = 388
    MSG_MHF_GET_UD_TACTICS_BONUS_QUEST = 389
    MSG_MHF_GET_UD_TACTICS_FIRST_QUEST_BONUS = 390
    MSG_MHF_GET_UD_TACTICS_REMAINING_POINT = 391
    MSG_SYS_reserve188 = 392
    MSG_MHF_LOAD_PLATE_MYSET = 393
    MSG_MHF_SAVE_PLATE_MYSET = 394
    MSG_SYS_reserve18B = 395
    MSG_MHF_GET_RESTRICTION_EVENT = 396
    MSG_MHF_SET_RESTRICTION_EVENT = 397
    MSG_SYS_reserve18E = 398
    MSG_SYS_reserve18F = 399
    MSG_MHF_GET_TREND_WEAPON = 400
    MSG_MHF_UPDATE_USE_TREND_WEAPON_LOG = 401
    MSG_SYS_reserve192 = 402
    MSG_SYS_reserve193 = 403
    MSG_SYS_reserve194 = 404
    MSG_MHF_SAVE_RENGOKU_DATA = 405
    MSG_MHF_LOAD_RENGOKU_DATA = 406
    MSG_MHF_GET_RENGOKU_BINARY = 407
    MSG_MHF_ENUMERATE_RENGOKU_RANKING = 408
    MSG_MHF_GET_RENGOKU_RANKING_RANK = 409
    MSG_MHF_ACQUIRE_EXCHANGE_SHOP = 410
    MSG_SYS_reserve19B = 411
    MSG_MHF_SAVE_MEZFES_DATA = 412
    MSG_MHF_LOAD_MEZFES_DATA = 413
    MSG_SYS_reserve19E = 414
    MSG_SYS_reserve19F = 415
    MSG_MHF_UPDATE_FORCE_GUILD_RANK = 416
    MSG_MHF_RESET_TITLE = 417
    MSG_SYS_reserve202 = 418
    MSG_SYS_reserve203 = 419
    MSG_SYS_reserve204 = 420
    MSG_SYS_reserve205 = 421
    MSG_SYS_reserve206 = 422
    MSG_SYS_reserve207 = 423
    MSG_SYS_reserve208 = 424
    MSG_SYS_reserve209 = 425
    MSG_SYS_reserve20A = 426
    MSG_SYS_reserve20B = 427
    MSG_SYS_reserve20C = 428
    MSG_SYS_reserve20D = 429
    MSG_SYS_reserve20E = 430
    MSG_SYS_reserve20F = 431
    
PacketTypeEnumValues = set(item.value for item in PacketType)


def main(target_process):
    # Attach to the process
    session = frida.attach(target_process)

    # Create our JS injected script:
    script = session.create_script("""
    const modName = "mhfo.dll";
    const encryptFunctionPattern = '55 8B EC 83 EC 10 0F B6 D2';
    const decryptFunctionPattern = '55 8B EC 83 EC 0C 8B 4D 0C 53 0F B6';

    // Some variables that will be initalized / calculated as the game is loaded.
    var mhfoMod;
    var encryptFunctionAddr;
    var decryptFunctionAddr;

    // Kick off our wait loop to get the mhfo.dll module.
    startGetModule();

    /*
    Interceptor.attach(Module.findExportByName("ws2_32.dll", "connect"), {
        onEnter: function(args) {
            //console.log("hooked connect");
            var buf = Memory.readByteArray(args[1], 16);
            send({hookType: "raw_connect"}, buf);
        }
    });

    
    Interceptor.attach(Module.findExportByName("ws2_32.dll", "send"), {
        onEnter: function(args) {
            console.log("hooked send");
            var buf = Memory.readByteArray(args[1], args[2].toInt32());
            send({hookType: "raw_send"}, buf);
        }
    });
    */


    // Modified version of https://gist.github.com/72lions/4528834
    function combineArrayBuffers(buf1, buf2, buf3) {
        var tmp = new Uint8Array(buf1.byteLength + buf2.byteLength + buf3.byteLength);
        tmp.set(new Uint8Array(buf1), 0);
        tmp.set(new Uint8Array(buf2), buf1.byteLength);
        tmp.set(new Uint8Array(buf3), buf1.byteLength + buf2.byteLength);
        return tmp.buffer;
    }

    function startGetModule() {
        // Guess whether the module is still packed or not depending on
        // whether or not the module is loaded when this is first called.
        try{
            mhfoMod = Process.getModuleByName(modName);
        }
        catch(err) {
            // It errored out, wait for the (packed) module to load and then unpack.
            console.log("Waiting for " + modName);
            waitForModuleToLoadAndUnpack();
            return;
        }

        // No error, module is probably unpacked already.
        console.log(modName + " is already loaded");
        doSigScanAndHook();
    }

    // Waits for the mhfo.dll module to be loaded and unpacked.
    // this works by hooking user32.dll$RegisterClassExA and waiting for
    // the mhfo.dll module to register the " M H F " class.
    function waitForModuleToLoadAndUnpack() {
        Interceptor.attach(Module.findExportByName("user32.dll", "RegisterClassExA"), {
            onEnter: function(args) {
                console.log("RegClass args[0] " + args[0]);
                var wndClassExA = args[0];
                var lpszClassName = wndClassExA.add(0x28).readPointer();
                var classNameStr = lpszClassName.readCString();
                var match = classNameStr == " M H F ";
                if(match) {
                    console.log("Module unloaded");
                    mhfoMod = Process.getModuleByName(modName);
                    doSigScanAndHook();
                }
            }
        });
    }

    function doSigScanAndHook() {
        // Sigscan for our functions
        var encResults = Memory.scanSync(mhfoMod.base, mhfoMod.size, encryptFunctionPattern);
        if (encResults < 1){
            console.log("Failed to find the encrypt function via sigscan");
            return;
        }

        var decResults = Memory.scanSync(mhfoMod.base, mhfoMod.size, decryptFunctionPattern);
        if (decResults < 1){
            console.log("Failed to find the decrypt function via sigscan");
            return;
        }

        // Use the first (and hopefully only) match as the address.
        encryptFunctionAddr = encResults[0].address;
        decryptFunctionAddr = decResults[0].address;

        // Finally hook the crypto funcs.
        hookCrypto();
    }

    function hookCrypto() {
        console.log('modBase: ' + mhfoMod.base);
        console.log('encryptFunctionAddr: ' + encryptFunctionAddr);
        console.log('decryptFunctionAddr: ' + decryptFunctionAddr);

        /*
        * The following hooked functions have a function signature like such:
        * this.context.ecx // data ptr
        * this.context.edx // unk
        * args[0] // CMessage_man*
        * args[1] // data ptr (again?)
        * args[2] // length
        * args[3] // cur write buf size / offset
        * args[4] // uint16_t[4]* 
        *
        * Additionally, the header doesn't get encrypted, only the body does, so we need to start
        * so we have to offset -14 bytes into the buffers and read +14 more bytes.
        */

        var encBufPtr;
        var encBufSize;
        var preEncryptBuf;
        var encSockAddrBuf;
        Interceptor.attach(encryptFunctionAddr, {
            onEnter: function(args){
                encBufPtr = args[1];
                encBufSize = args[2].toInt32();
                preEncryptBuf = Memory.readByteArray(encBufPtr.sub(14), encBufSize+14);

                var sockManPtr = args[0].add(4).readPointer();
                var sockAddrPtr = sockManPtr.add(0x34);
                encSockAddrBuf = Memory.readByteArray(sockAddrPtr, 16);
            },
            onLeave: function(args){
                var postEncryptBuf = Memory.readByteArray(encBufPtr.sub(14), encBufSize+14);
                var sendBuf = combineArrayBuffers(preEncryptBuf, postEncryptBuf, encSockAddrBuf);
                send({
                        hookType: "encrypt",
                        preBufSize: preEncryptBuf.byteLength,
                        postBufSize: postEncryptBuf.byteLength,
                    }, sendBuf);
            }
        });

        var decBufPtr;
        var decBufSize;
        var preDecryptBuf;
        var decSockAddrBuf;
        Interceptor.attach(decryptFunctionAddr, {
            onEnter: function(args){
                decBufPtr = args[1];
                decBufSize = args[2].toInt32();
                preDecryptBuf = Memory.readByteArray(decBufPtr.sub(14), decBufSize+14);

                var sockManPtr = args[0].add(4).readPointer();
                var sockAddrPtr = sockManPtr.add(0x34);
                decSockAddrBuf = Memory.readByteArray(sockAddrPtr, 16);
            },
            onLeave: function(args){
                var postDecryptBuf = Memory.readByteArray(decBufPtr.sub(14), decBufSize+14);
                var sendBuf = combineArrayBuffers(preDecryptBuf, postDecryptBuf, decSockAddrBuf);
                send({
                        hookType: "decrypt",
                        preBufSize: preDecryptBuf.byteLength,
                        postBufSize: postDecryptBuf.byteLength,
                    }, sendBuf);
            }
        });

    }
    """)



    def on_message(message, data):
        if message['type'] == 'error':
            print(message)
            return
        elif message['payload']['hookType'] == "encrypt" or message['payload']['hookType'] == "decrypt":
            pre_buf_size = message['payload']['preBufSize']
            post_buf_size = message['payload']['postBufSize']
            is_encrypt = message['payload']['hookType'] == "encrypt"

            pre_buf = data[:pre_buf_size]
            post_buf = data[pre_buf_size:pre_buf_size+post_buf_size]
            sock_addr_buf = data[pre_buf_size+post_buf_size:]

            # Figure out which one buffer is which.
            decrypted_buf = pre_buf if is_encrypt else post_buf
            encrypted_buf = pre_buf if not is_encrypt else post_buf

            # Print direction.
            print('')
            print("Outgoing" if is_encrypt else "Incoming")

            # Print IP:port.
            (family, port, ip_byte_0, ip_byte_1, ip_byte_2, ip_byte_3) = struct.unpack(">HHBBBB", sock_addr_buf[:8])
            print("{}.{}.{}.{}:{}".format(ip_byte_0, ip_byte_1, ip_byte_2, ip_byte_3, port))

            # Print time.
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

            packet_op = struct.unpack(">H", decrypted_buf[14:16])[0]
            packet_type_str = '<Unknown packet>' if not packet_op in PacketTypeEnumValues else PacketType(packet_op).name
            print(packet_type_str)

            # Print ascii representation.
            """
            for k, v in enumerate(decrypted_buf):
                if v > 0x21 and v < 0x7E:
                    print(chr(v), end='')
                else:
                    print('.', end='')
            print('', end='\n', flush=True)
            """

            # Print the buffers as spaced hex.
            def print_spaced_hex(b):
                s = binascii.hexlify(b).upper().decode()
                print(' '.join(s[i:i+2] for i in range(0, len(s), 2)))

            print_spaced_hex(encrypted_buf)
            print_spaced_hex(decrypted_buf)
        else:
            pass
            print("[%s] => %s" % (message, data))
    script.on('message', on_message)
    script.load()
    
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} mhf.exe".format(sys.argv[0]))
        sys.exit(1)

    main(sys.argv[1])
