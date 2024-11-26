import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
} #辞書の追加
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外化を判定する
    引数:こうかとんRect Or 爆弾Rect
    戻り値：真理値タプル（横、縦）/画面内:True、画面外:False   
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    戻り値:
        bb_imgs (list[pg.Surface]): 爆弾サイズに応じたSurfaceのリスト
        bb_accs (list[int]): 爆弾の加速度のリスト
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト（1〜10）
    
    # サイズが異なる爆弾Surfaceのリストを作成
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)  # 爆弾用のSurface
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 爆弾円を描画
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する
    画面をブラックアウト（半透明）
    泣いているこうかとん画像と「Game Over」の文字列を表示
    5秒間待機
    """
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))
    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.5)
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    offset_x = 25
    screen.blit(text, text_rect)
    screen.blit(cry_kk_img, (text_rect.left - offset_x - cry_kk_img.get_width(),
                             text_rect.centery - cry_kk_img.get_height() // 2))
    screen.blit(cry_kk_img, (text_rect.right + offset_x,
                             text_rect.centery - cry_kk_img.get_height() // 2))
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾の初期化
    bb_imgs, bb_accs = init_bb_imgs()  # サイズと加速度のリストを取得
    bb_rct = bb_imgs[0].get_rect()  # 爆弾の最初のサイズ
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)  # ゲームオーバー画面を表示
            return  # ゲームを終了
        screen.blit(bg_img, [0, 0])
        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # 辞書の引用
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 時間経過による爆弾の拡大と加速
        idx = min(tmr // 500, 9)  # インデックスの上限は9
        avx = vx * bb_accs[idx]  # 加速された速度
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]  # 現在のサイズの爆弾
        # 爆弾の中心を維持
        bb_rct = bb_img.get_rect(center=bb_rct.center) 
        # 爆弾の移動
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        # 爆弾の描画
        screen.blit(bb_img, bb_rct)
        tmr += 1
        pg.display.update()
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
