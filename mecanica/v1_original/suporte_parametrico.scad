/* Henrique | Protótipo V1 | unidades: mm
   Fan: 58 x 58 x 15. TCRT5000 avulso: 10 x 5 x 5, informado.
   Montagem com sensor frontal e alvo branco traseiro localizado.
   A distância óptica nominal é ~19.1 mm: validar eletricamente ANTES
   de imprimir. Isto não garante a leitura do alvo pelo TCRT5000.
   Rotação, cubo e travessas reais da ventoinha ainda não foram medidos.
   Abra part="assembly" para montagem; "layout" para peças de impressão.
*/
part = "integral";
$fn = 48;

fan_w = 58;
fan_h = 58;
fan_depth = 15;
fan_clearance_side = 0.40;
wall = 3.5;
lip_height = 1.5;
lip_opening = 56.5;
frame_depth = 18;

sensor_w = 10;
sensor_h = 5;
sensor_depth = 5;
sensor_clearance_side = 0.20;
sensor_radial = 19;           // deslocamento nominal em Y, ajustável +/-5
sensor_front_gap = 2;        // distância lente / face frontal da ventoinha
target_radial = 19;          // alinhar com sensor, ajustável +/-5
target_w = 16;
target_h = 12;
rear_spacer_height = 0.6;    // distância alvo/face traseira = 2.1 mm

mount_y = 42;
mount_hole_d = 3.4;
arm_thickness = 3;
radial_adjust = 5;
sensor_floor_top = 4.5;
sensor_wall_top = sensor_floor_top + sensor_depth - 0.5;
sensor_optical_z = sensor_floor_top + sensor_depth;
front_arm_z = lip_height - sensor_front_gap - sensor_optical_z;
front_spacer_height = -front_arm_z - arm_thickness;
rear_arm_z = frame_depth + rear_spacer_height;

inner_w = fan_w + 2*fan_clearance_side;
inner_h = fan_h + 2*fan_clearance_side;
outer_w = inner_w + 2*wall;
outer_h = inner_h + 2*wall;
sensor_iw = sensor_w + 2*sensor_clearance_side;
sensor_ih = sensor_h + 2*sensor_clearance_side;

echo("Optical distance sensor / white target (mm)",
     rear_arm_z - (lip_height-sensor_front_gap));
echo("Front spacer height (mm)", front_spacer_height);

module rr(w,h,r=2) {
  offset(r=r) square([w-2*r,h-2*r],center=true);
}
module slot_y(y0,y1,d,h) {
  hull() {
    translate([0,y0,0]) cylinder(d=d,h=h);
    translate([0,y1,0]) cylinder(d=d,h=h);
  }
}

module frame() {
  difference() {
    union() {
      linear_extrude(frame_depth) rr(outer_w,outer_h,2.2);
      // A aba fica fora da passagem de ar; não usa os furos da ventoinha.
      translate([-9,outer_h/2-1,0])
        cube([18,52-(outer_h/2-1),frame_depth]);
    }
    // Encaixe de 58.8 x 58.8, com lábio de apoio frontal.
    translate([-inner_w/2,-inner_h/2,lip_height])
      cube([inner_w,inner_h,frame_depth+1]);
    translate([-lip_opening/2,-lip_opening/2,-0.2])
      cube([lip_opening,lip_opening,lip_height+0.4]);
    translate([0,mount_y,-0.2]) cylinder(d=mount_hole_d,h=frame_depth+0.4);
    // Janela de carregamento lateral: permite inserir a ventoinha em +X
    // mesmo com os dois braços já fundidos à moldura na versão integral.
    // O lábio z=0..1.5 permanece como guia, abaixo da carcaça.
    translate([inner_w/2-0.1,-inner_h/2,lip_height])
      cube([wall+1,inner_h,frame_depth+1]);
    // Pilotos para dois parafusos M3 apertados levemente na carcaça fixa.
    // Não correspondem aos furos originais da ventoinha.
    for(x=[-24,24])
      translate([x,fan_h/2-1,lip_height+fan_depth/2])
        rotate([-90,0,0]) cylinder(d=2.8,h=wall+4);
  }
}

module front_arm() {
  difference() {
    union() {
      translate([-7,12,0]) cube([14,39.5,arm_thickness]);
      // Assento aberto, com passagem dos quatro terminais pelo fundo.
      translate([-(sensor_iw+4)/2,sensor_radial-(sensor_ih+4)/2,arm_thickness])
        cube([sensor_iw+4,sensor_ih+4,sensor_wall_top-arm_thickness]);
    }
    translate([-sensor_iw/2,sensor_radial-sensor_ih/2,sensor_floor_top])
      cube([sensor_iw,sensor_ih,sensor_depth+4]);
    translate([-4.4,sensor_radial-1.7,-0.2]) cube([8.8,3.4,sensor_floor_top+0.4]);
    translate([0,0,-0.2])
      slot_y(mount_y-radial_adjust,mount_y+radial_adjust,mount_hole_d,arm_thickness+0.4);
  }
}

module rear_arm() {
  difference() {
    union() {
      translate([-5,target_radial,0]) cube([10,51.5-target_radial,arm_thickness]);
      // O alvo branco vai na face z=0, voltada ao sensor.
      translate([-target_w/2,target_radial-target_h/2,0])
        cube([target_w,target_h,arm_thickness]);
    }
    translate([0,0,-0.2])
      slot_y(mount_y-radial_adjust,mount_y+radial_adjust,mount_hole_d,arm_thickness+0.4);
  }
}

module spacer(h) {
  difference() {
    cylinder(d=10,h=h);
    translate([0,0,-0.2]) cylinder(d=mount_hole_d,h=h+0.4);
  }
}

module fan_reference() {
  // Somente referência visual. Não é peça para imprimir nem rotor medido.
  translate([0,0,lip_height]) {
    difference() {
      linear_extrude(fan_depth) rr(fan_w,fan_h,3);
      translate([0,0,-0.1]) cylinder(d=54,h=fan_depth+0.2);
    }
    cylinder(d=20,h=fan_depth);
    for(a=[0:60:300]) rotate([0,0,a]) translate([0,0,fan_depth/2])
      linear_extrude(1) polygon([[8,-2],[25,-4],[24,6],[11,7]]);
  }
}

module assembly(explode=0,reference=true) {
  color("slategray") frame();
  translate([0,0,front_arm_z-explode]) color("darkorange") front_arm();
  translate([0,mount_y,-front_spacer_height-explode/2])
    color("silver") spacer(front_spacer_height);
  translate([0,0,rear_arm_z+explode]) color("white") rear_arm();
  translate([0,mount_y,frame_depth+explode/2])
    color("silver") spacer(rear_spacer_height);
  if(reference) %color([0.15,0.25,0.35,0.35]) fan_reference();
}

if(part=="frame") frame();
else if(part=="front_arm") front_arm();
else if(part=="rear_arm") rear_arm();
else if(part=="front_spacer") spacer(front_spacer_height);
else if(part=="rear_spacer") spacer(rear_spacer_height);
else if(part=="reference_fan") fan_reference();
else if(part=="integral") translate([0,0,-front_arm_z]) union() {
  frame();
  translate([0,0,front_arm_z]) front_arm();
  translate([0,0,rear_arm_z]) rear_arm();
  // Sobreposição de 0.03 mm evita faces apenas tangentes na união.
  translate([0,mount_y,-front_spacer_height-0.03]) spacer(front_spacer_height+0.06);
  translate([0,mount_y,frame_depth-0.03]) spacer(rear_spacer_height+0.06);
}
else if(part=="exploded") assembly(12);
else if(part=="layout") {
  frame();
  translate([55,0,0]) front_arm();
  translate([80,0,0]) rear_arm();
  translate([55,-15,0]) spacer(front_spacer_height);
  translate([80,-15,0]) spacer(rear_spacer_height);
}
else assembly();
