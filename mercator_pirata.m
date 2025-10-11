%% =======================================================================
% CIPMA-CHAIRE UNESCO
% M2 OPA 2025
% TP1 Matlab / TP2
% EBOLO NKONGO VICTOR
% 10/10/2025
% =======================================================================

clear all; close all; clc;

%% 
% A/ Température à l'équateur 10°W–2°E (Mercator)

% 1/ Lecture des variables Mercator
load("C:\Users\ebolo\Downloads\TP_matlab\J2\data2\depth_mercator.mat");
load("C:\Users\ebolo\Downloads\TP_matlab\J2\data2\lat_mercator.mat");
load("C:\Users\ebolo\Downloads\TP_matlab\J2\data2\lon_mercator.mat");
load("C:\Users\ebolo\Downloads\TP_matlab\J2\data2\temp_mercator.mat");

% 2/ Équateur, 10°W–2°E
ilon = find(longi >= -10 & longi <= 2);
ilat = find(lat == 0);
lon = longi(ilon);
lats = lat(ilat);
temp = Temp(ilon, ilat, :);

% 3/ à 300 m
ildep = find(depth >= 0 & depth <= 300);
dep = depth(ildep);
temp300 = Temp(ilon, ilat, ildep);

% 4/ Visualisation avec contourf
figure(1)
contourf(lon, dep, squeeze(temp300)')
colorbar
caxis([10 30])
colormap('jet')
xlabel('Longitude')
ylabel('Profondeur (m)')
title('Température Mercator Équateur (0–300 m)')
axis ij
grid on

%% 
% B/ Transect à 10°W, 3°S–3°N (Mercator)


ilon = find(longi >= -10 & longi <= -10);   
ilat = find(lat >= -3 & lat <= 3);
lon = longi(ilon);
lats = lat(ilat);
temp = squeeze(Temp(ilon, ilat, :));

% à 300 m
ildep = find(depth >= 0 & depth <= 300);
dep = depth(ildep);
temp300 = temp(:, ildep);

% Visualisation
figure(2)
contourf(lats, dep, temp300')
colorbar
caxis([10 30])
colormap('jet')
xlabel('Latitude')
ylabel('Profondeur (m)')
title('Température Mercator à 10°W (3°S–3°N, 0–300 m)')
axis ij
grid on

%% 
% C/ Comparaison Mercator vs PIRATA

% Lecture des données PIRATA
file = 'C:\Users\ebolo\Downloads\TP_matlab\J2\data2\pirata-fr23_ctd.nc';
sss   = ncread(file, 'PSAL');
sst   = ncread(file, 'TEMP');
lonp  = ncread(file, 'LONX');
latp  = ncread(file, 'LATX');
pres  = ncread(file, 'PRES');
a=lonp(ip);
% 10°W, 3°S–3°N
ip= find(lonp >= -10 & lonp <= -9 & latp >= -3 & latp <= 3);
%ip=find(abs(lonp+10)<0.1)
latp_sel = latp(ip);
sst_sel  = sst(:, ip);
pres_sel = pres(:, ip);

% à 300 m
ipres = find(pres(:,1) <= 300);
pres300 = pres(ipres,1);
sst300  = sst_sel(ipres,:);

% Suppression des doublons et tri des latitudes
[latp_unique, ia, ~] = unique(latp_sel, 'stable');
sst300_unique = sst300(:, ia);

% Tri croissant
[latp_unique, ind] = sort(latp_unique);
sst300_unique = sst300_unique(:, ind);

% Comparaison
figure(10)

subplot(1,2,1)
contourf(lats, dep, temp300')
colorbar
caxis([10 30])
colormap('jet')
xlabel('Latitude')
ylabel('Profondeur (m)')
title('Mercator 10°W (3°S–3°N, 0–300 m)')
axis ij
grid on

subplot(1,2,2)
contourf(latp_unique, pres300, sst300_unique)
colorbar
caxis([10 30])
colormap('jet')
xlabel('Latitude')
ylabel('Pression (dbar)')
title('PIRATA FR23 10°W (3°S–3°N, 0–300 m)')
axis ij
grid on

%%
% D/ Profil moyen comparatif (Mercator vs PIRATA)


figure(8)

% Mercator
prof_mer = mean(temp300,1);  % moyenne sur les latitudes
plot(prof_mer, dep, 'r-', 'LineWidth',2); hold on

% PIRATA
prof_pir = mean(sst300_unique,2);   % moyenne sur les stations
plot(prof_pir, pres300, 'b--', 'LineWidth',2);

% Inverser l'axe des profondeurs
axis ij

xlabel('Température (°C)')
ylabel('Profondeur (m)')
legend('Mercator','PIRATA FR23','Location','Best')
title('Profil moyen de température : Mercator vs PIRATA (0–300 m)')
grid on
