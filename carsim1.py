import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Supercar simulator")
clock = pygame.time.Clock()

IDLE_RPM = 900
REDLINE = 9000
ENGINE_TORQUE = 750
ENGINE_DRAG = 2200
VEHICLE_MASS = 1280
WHEEL_RADIUS = 0.34
FINAL_DRIVE = 3.60
AIR_DRAG = 0.30
BRAKE_FORCE =  16000


GEAR_RATIOS = {
    1: 3.10,
    2: 2.15,
    3: 1.65,
    4: 1.30,
    5: 1.05,
    6: 0.84,
    7: 0.67
}

rpm  = IDLE_RPM
speed = 0.0
gear = 1

display_rpm = rpm
display_speed = speed

throttle = 0.0
brake = 0.0
clutch = 0.0
display_wheelspin = 0.0

LAUNCH_RPM = 4200
LAUNCH_SPEED_CUTOFF = 5 / 3.6   # 5 km/h in m/s


# Function defined to keep variable within bounds
def clamp( x, lo, hi):
    return max(lo,min(x,hi))



# drawing functions


def draw_bar( x,y,w,h, value, color):
    pygame.draw.rect(screen, (40,40,40), (x,y,w,h))
    pygame.draw.rect(screen, color, ( x,y,w*value,h) )



def draw_gauge( cx, cy, r, value, vmin, vmax, label, unit, redline=None):
    START_DEG = 225
    SWEEP_DEG = 270
    pygame.draw.circle(screen, (45,45,45), (cx,cy), r, 6)

    if redline is not None:
        rl_ratio = ( redline-vmin)/(vmax-vmin)
        rl_deg = START_DEG - rl_ratio*SWEEP_DEG

        pygame.draw.arc(
            screen, (220,60,60),
                (cx-r,cy-r,r*2,r*2),
                    math.radians(rl_deg),
                    math.radians(START_DEG-SWEEP_DEG),
                    6    
                    )
    
    ratio = clamp( (value-vmin)/(vmax-vmin) , 0, 1)
    angle_deg = START_DEG - ratio*SWEEP_DEG
    angle = math.radians(angle_deg)

    nx = cx + r*0.85*math.cos(angle)
    ny = cy - r*0.85*math.sin(angle)

    pygame.draw.line(screen, (240,240,240), (cx,cy), (nx,ny), 4)
    pygame.draw.circle(screen, (240, 240, 240), (cx,cy), 6)

    font = pygame.font.SysFont(None, 28)
    screen.blit(font.render(label, True, (230,230,230)), (cx-35, cy+r-25))

    screen.blit(
        font.render( f"{int(value)} {unit}", True, (230,230,230) ),
        (cx-45,cy+r+5)
    )

    screen.blit(font.render( str(gear), True, (230,230,230)), (550,300))


# Main Loop
    
    

running = True
while running:
    dt = clock.tick(60)/1000


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_s and gear<7:
                gear+=1
            if event.key == pygame.K_a and gear>1:
                gear-=1
    keys =  pygame.key.get_pressed()      



    throttle = 1.0 if keys[pygame.K_UP] else 0.0
    brake = 1.0 if keys[pygame.K_DOWN] else 0.0

    if keys[pygame.K_z]:
        clutch += dt*4
    else:
        clutch -= dt*4
    clutch = clamp(clutch,0,1)

    launch_control_active = (
        gear == 1 and
        speed < LAUNCH_SPEED_CUTOFF and
        throttle > 0.9 and
        clutch < 0.1
    )
    effective_throttle = throttle
    if launch_control_active:
        rpm_error = rpm - LAUNCH_RPM
        if rpm_error > 0:
            effective_throttle -= rpm_error / 3000
            effective_throttle = clamp(effective_throttle, 0, 1)




# MECHANICS



    # Engine rpm evolution

    rpm += ( effective_throttle * 6500 - ENGINE_DRAG)*dt
    

    # Drive-train coupling

    if clutch < 0.1 and not launch_control_active:
        wheel_rpm = ( speed/ (2*math.pi*WHEEL_RADIUS)) * 60
        target_rpm = wheel_rpm *GEAR_RATIOS[gear] * FINAL_DRIVE
        rpm += ( target_rpm-rpm)*dt*12
    rpm = clamp( rpm, IDLE_RPM, REDLINE)


    # Torque curve

    rpm_ratio = rpm / REDLINE
    torque_factor = max( 0.0, 1.0 - rpm_ratio**1.7)

    # Engine Torque Production

    engine_torque = ENGINE_TORQUE*torque_factor*effective_throttle

    # Torque through transmission

    wheel_torque = engine_torque*GEAR_RATIOS[gear]*FINAL_DRIVE*(1-clutch)

    # Torque force conversion

    raw_drive_force =  wheel_torque / WHEEL_RADIUS
    MAX_TRACTION_FORCE = VEHICLE_MASS * 9.81 * 1.2  # μ ≈ 1.2 (supercar tire)

    drive_force = clamp(raw_drive_force, -MAX_TRACTION_FORCE, MAX_TRACTION_FORCE)
    wheelspin_ratio = abs(raw_drive_force) / MAX_TRACTION_FORCE


    # Retarding forces

    drag_force = AIR_DRAG*speed*speed
    brake_force = BRAKE_FORCE * brake

    # Newtonian equations

    acceleration = (drive_force-drag_force-brake_force)/VEHICLE_MASS
    speed += acceleration*dt
    speed = max( speed , 0)



    # DISPLAY

    display_rpm = rpm
    display_speed = speed
    screen.fill((15,15,15))
    draw_gauge(300, 300, 180, display_rpm, 0, REDLINE, "RPM", "", redline=REDLINE*0.85)
    draw_gauge(800, 300, 180, display_speed*3.6, 0, 350, "Speed", "km/h", redline = None)
    display_wheelspin += (wheelspin_ratio - display_wheelspin) * dt * 10
    display_wheelspin = clamp(display_wheelspin, 0, 2)

    draw_bar(
    450, 460, 200, 15,
    clamp(display_wheelspin, 0, 1),
    (220, 220, 220) if display_wheelspin < 1
    else (220, 60, 60)
    )
    if launch_control_active:
        font = pygame.font.SysFont(None, 32)
        screen.blit(
            font.render("LAUNCH", True, (60, 200, 255)),
            (520, 330)
    )




    pygame.display.flip()



