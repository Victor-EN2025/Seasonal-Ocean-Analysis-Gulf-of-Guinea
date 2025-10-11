%% ======================================================================
% CIPMA-CHAIRE UNESCO
% M2 OPA 2025
% TP1 Matlab
% Auteur : EBOLO NKONGO VICTOR
% Date : 11/10/2025
% ======================================================================
% TP 3 : Visualisation de données océanographiques
% - Lecture de fichiers NetCDF
% - Tracé de température, salinité et pression le long du méridien 10°W
% - Calcul de climatologie et anomalies SST
% ======================================================================

clear; close all; clc;

%% ===========================
% 1. Lecture des données NetCDF
% ===========================
file = 'C:\Users\ebolo\Downloads\TP_matlab\J3\data3\mercatorpsy3v3r1_tat_mean_20110125_R20110112.nc';

sst = ncread(file, 'temperature');   % Température [K]
sss = ncread(file, 'salinity');      % Salinité
lat = ncread(file, 'latitude');      % Latitude
lon = ncread(file, 'longitude');     % Longitude
dep = ncread(file, 'depth');         % Profondeur

% Conversion de la température en °C
sst = sst - 271.15;

%% ===========================
% 2. Extraction le long du méridien 10°W
% ===========================
[~, ix] = min(abs(lon + 10));           % Indice proche de 10°W
id200 = dep >= 0 & dep <= 200;          % Profondeur jusqu'à 200 m
dep200 = dep(id200);

% Extraction des sections
temp_section = squeeze(sst(ix, :, id200));   % Température le long de 10°W
temp_surface = squeeze(sst(:, :, 1));       % Température de surface
sss_section = squeeze(sss(ix, :, id200));   % Salinité le long de 10°W
sss_surface = squeeze(sss(:, :, 1));        % Salinité de surface

%% ===========================
% 3. Cartes de surface
% ===========================
figure('Name','Cartes de surface','NumberTitle','off')

subplot(1,2,1)
contourf(lon, lat, temp_surface', 10, 'LineColor', 'none')
colorbar; colormap('jet')
xlabel('Longitude'); ylabel('Latitude')
title('Température (°C) surface')
grid on

subplot(1,2,2)
contourf(lon, lat, sss_surface', 10, 'LineColor', 'none')
colorbar; caxis([33 36]); colormap('jet')
xlabel('Longitude'); ylabel('Latitude')
title('Salinité surface')
grid on

%% ===========================
% 4. Profils verticaux le long de 10°W
% ===========================
figure('Name','Profil le long de 10°W - Température','NumberTitle','off')
contourf(lat, dep200, temp_section', 10, 'LineColor', 'none')
colorbar; colormap('jet'); caxis([18 20])
xlabel('Latitude'); ylabel('Profondeur (m)')
title('Température (°C) le long de 10°W')
axis ij; grid on

figure('Name','Profil le long de 10°W - Salinité','NumberTitle','off')
contourf(lat, dep200, sss_section', 10, 'LineColor', 'none')
colorbar; colormap('jet')
xlabel('Latitude'); ylabel('Profondeur (m)')
title('Salinité le long de 10°W')
axis ij; grid on

%% ===========================
% 5. Lecture des séries SST mensuelles
% ===========================
datamax = readtable("TempMensMax.dat");
datamin = readtable("TempMensMin.dat");

time_max = datamax{:,1}; sstmax = datamax{:,2};
time_min = datamin{:,1}; sstmin = datamin{:,2};

% Extraction année et mois
[an_max, mois_max] = deal(floor(time_max/100), mod(time_max,100));
[an_min, mois_min] = deal(floor(time_min/100), mod(time_min,100));

% Climatologie mensuelle
clim_max = arrayfun(@(m) mean(sstmax(mois_max==m),'omitnan'), 1:12)';
clim_min = arrayfun(@(m) mean(sstmin(mois_min==m),'omitnan'), 1:12)';

% Anomalies
anom_max = sstmax - clim_max(mois_max);
anom_min = sstmin - clim_min(mois_min);

% Dates
tmax = datetime(an_max, mois_max, 15);
tmin = datetime(an_min, mois_min, 15);

%% ===========================
% 6. Tracé SST
% ===========================
figure('Name','SST max/min et anomalies','NumberTitle','off')

% SST max et min
subplot(3,1,1)
plot(tmax, sstmax, 'r', tmin, sstmin, 'b', 'LineWidth', 1.2)
xlabel('Année'); ylabel('SST (°C)')
title('SST max et min')
legend('Max','Min','Location','best'); grid on

% Anomalies SST
subplot(3,1,2)
plot(tmax, anom_max, 'r', tmin, anom_min, 'b')
xlabel('Année'); ylabel('Anomalie (°C)')
title('Anomalies mensuelles SST')
legend('Max','Min','Location','best'); grid on

% Cycle saisonnier moyen
subplot(3,1,3)
plot(1:12, clim_max, '-or', 1:12, clim_min, '-ob', 'LineWidth', 1.2)
xlabel('Mois'); ylabel('SST moyenne (°C)')
title('Cycle saisonnier moyen')
legend('Max','Min','Location','best'); grid on
