% CIPMA-CHAIRE UNESCO
% M2 OPA 2025
%TP1 Matlab
%C EBOLO NKONGO VICTOR
%09 Decembre 2025

%=======================================================================================================================
% TP 3
 
% utiliser fichiers".nc" et tracer de plusieurs variables en utilisant les donnees data3
%=======================================================================================================================

%A/
% 1/ lire les variables contenus dans le repertoire data3 (données Mercator et Pirata)

% 2/ tracer Temperature, salinite, pression le long de 10°W

clear; close all; clc;


file = 'C:\Users\ebolo\Downloads\TP_matlab\J3\data3\mercatorpsy3v3r1_tat_mean_20110125_R20110112.nc';


sst = ncread(file, 'temperature');  
sss = ncread(file, 'salinity');      
lat = ncread(file, 'latitude');
lon = ncread(file, 'longitude');
dep = ncread(file, 'depth');
%time=ncread(file,'time');

sst=sst-271.15;


[~, ix] = min(abs(lon + 10)); 
id=find(dep>=0 & dep<=200);
dep200=dep(id);

temps = squeeze(sst(ix, :, id));  
tempsur = squeeze(sst(:, :, 1));  
sss_se = squeeze(sss(ix, :, id));  
sss_sur = squeeze(sss(:, :, 1));  


%%
%carte
figure(1)
subplot(1,2,1)

contourf(lon, lat, tempsur', 10, 'LineColor', 'none');
colorbar
colormap('jet')
xlabel('longitude')
ylabel('latitude')
title('Température (°C) surface')
grid on
subplot(1,2,2)









contourf(lon, lat, sss_sur', 10, 'LineColor', 'none');
colorbar
caxis([33 36])

colormap('jet')
xlabel('longitude')
ylabel('latitude')
title('sss surface')
grid on

%profil a 200

figure(3)
contourf(lat, dep200, temps', 10, 'LineColor', 'none');
colorbar
colormap('jet')
caxis([18 20])
xlabel('Latitude')
ylabel('Profondeur (m)')
title('Température (°C) le long de 10°W')
axis ij
grid on

figure(4)
contourf(lat, dep300, temps', 10, 'LineColor', 'none');
colorbar
colormap('jet')
caxis([18 20])
xlabel('Latitude')
ylabel('Profondeur (m)')
title('Température (°C) le long de 10°W')
axis ij
grid on





figure(3)
contourf(lon, lat, sss_sur', 20, 'LineColor', 'none');
colorbar
colormap('jet')
xlabel('longitude')
ylabel('latitude')
title('sss surface')
grid on
figure(4)
contourf(lat, dep200, sss_se', 10, 'LineColor', 'none');
colorbar
colormap('jet')
xlabel('Latitude')
ylabel('Profondeur (m)')
title('sss le long de 10°W')
axis ij
grid on




datamax = readtable("TempMensMax.dat");
datamin = readtable("TempMensMin.dat");

time_max = datamax{:,1}; sstmax = datamax{:,2};
time_min = datamin{:,1}; sstmin = datamin{:,2};


[an_max, mois_max] = deal(floor(time_max/100), mod(time_max,100));
[an_min, mois_min] = deal(floor(time_min/100), mod(time_min,100));


clim_max = arrayfun(@(m) mean(sstmax(mois_max==m),'omitnan'), 1:12)';
clim_min = arrayfun(@(m) mean(sstmin(mois_min==m),'omitnan'), 1:12)';


anom_max = sstmax - clim_max(mois_max);
anom_min = sstmin - clim_min(mois_min);


tmax = datetime(an_max, mois_max, 15);
tmin = datetime(an_min, mois_min, 15);


figure(1);

subplot(3,1,1)
plot(tmax, sstmax, 'r', tmin, sstmin, 'b', 'LineWidth', 1.2)
xlabel('Année'); ylabel('sst (°C)')
title('ssts max et min')
legend('Max','Min','Location','best');
grid on

subplot(3,1,2)
plot(tmax, anom_max, 'r', tmin, anom_min, 'b')
xlabel('Année'); ylabel('Anomalie (°C)')
title('Anomalies mensuel sst')
legend('Max','Min','Location','best'); 
grid on

subplot(3,1,3)
plot(1:12, clim_max, '-or', 1:12, clim_min, '-ob', 'LineWidth', 1.2)
xlabel('Mois'); ylabel('sst moyenne (°C)')
title('Cycle saisonnier moyen')
legend('Max','Min','Location','best'); 
grid on

